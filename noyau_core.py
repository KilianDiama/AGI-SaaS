#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Unified PerfectAI Engine – Kernel
Consolidated and optimized core engine with plugin management, observability, FastAPI, WebSocket, and CLI.
"""
from __future__ import annotations
import argparse
import asyncio
import importlib
import inspect
import logging
import os
import pkgutil
import pkg_resources
import signal
import sys
import time
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Protocol, runtime_checkable, Optional
from dotenv import load_dotenv

load_dotenv()

import uvicorn
from fastapi import FastAPI, HTTPException, Request, Response, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings
from prometheus_client import Counter, Histogram, Gauge, generate_latest

# —————————————————————————————————————————————————————————————————————
# Configuration
# —————————————————————————————————————————————————————————————————————

class Settings(BaseSettings):
    app_name: str = Field("PerfectAI Engine", env="APP_NAME")
    version: str = Field("1.0.0", env="VERSION")
    host: str = Field("0.0.0.0", env="HOST")
    port: int = Field(8000, env="PORT")
    debug: bool = Field(False, env="DEBUG")
    plugin_package: str = Field("plugins", env="PLUGIN_PACKAGE")
    master_key: Optional[str] = Field(None, env="MASTER_KEY")
    concurrency_limit: int = Field(10, env="CONCURRENCY_LIMIT")
    enable_metrics: bool = Field(True, env="ENABLE_METRICS")
    cors_origins: List[str] = Field(["*"], env="CORS_ORIGINS")
    openrouter_api_key: str = Field("", env="OPENROUTER_API_KEY")
    ollama_base_url: str = Field("http://localhost:11434", env="OLLAMA_BASE_URL")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "allow"  # ← autorise les variables supplémentaires

settings = Settings()

# —————————————————————————————————————————————————————————————————————
# Logging
# —————————————————————————————————————————————————————————————————————

LOG_FMT = "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
logging.basicConfig(
    stream=sys.stdout,
    level=logging.DEBUG if settings.debug else logging.INFO,
    format=LOG_FMT
)
logger = logging.getLogger("perfectai.core")

# —————————————————————————————————————————————————————————————————————
# Vault & Cache stubs
# —————————————————————————————————————————————————————————————————————

class Vault:
    def __init__(self, addr: str = ""):
        self.addr = addr
    async def get_secret(self, key: str) -> str:
        return os.environ.get(key, "")

vault = Vault()

class CacheClient:
    def __init__(self, addr: Optional[str] = None):
        self.addr = addr
        self._store: Dict[str, Any] = {}
    async def get(self, key: str) -> Any:
        return self._store.get(key)
    async def set(self, key: str, value: Any, expire: Optional[int] = None) -> None:
        self._store[key] = value

cache = CacheClient()

# —————————————————————————————————————————————————————————————————————
# Telemetry
# —————————————————————————————————————————————————————————————————————

REQ_COUNT = Counter("pai_http_requests_total", "Total HTTP requests")
REQ_LAT   = Histogram("pai_http_request_latency_seconds", "HTTP request latency (s)")
PLUGIN_LAT = Histogram("pai_plugin_latency_seconds", "Plugin execution latency", ["plugin"])
PLUGIN_ERR = Counter("pai_plugin_errors_total", "Plugin execution errors", ["plugin"])
SHUTDOWN_GAUGE = Gauge("pai_shutdown_flag", "Shutdown indicator (1 if shutting down)")

# —————————————————————————————————————————————————————————————————————
# Plugin protocol & base
# —————————————————————————————————————————————————————————————————————

Context = Dict[str, Any]

@runtime_checkable
class Plugin(Protocol):
    meta: Meta
    async def before(self, ctx: Context) -> None: ...
    async def run(self, ctx: Context) -> Context: ...
    async def after(self, ctx: Context) -> None: ...

@dataclass
class Meta:
    name: str
    priority: int = 100
    version: str = "0.1"
    author: str = "anonymous"

class BasePlugin:
    meta: Meta = Meta(name="base")
    async def before(self, ctx: Context) -> None: pass
    async def run(self, ctx: Context) -> Context:
        raise NotImplementedError
    async def after(self, ctx: Context) -> None: pass

# —————————————————————————————————————————————————————————————————————
# Plugin manager
# —————————————————————————————————————————————————————————————————————

class PluginManager:
    def __init__(self):
        self._plugins: Dict[str, BasePlugin] = {}
        self._discover_local()
        self._discover_entrypoints()

    def _register(self, inst: BasePlugin):
        self._plugins[inst.meta.name] = inst
        logger.info("🔌 Plugin registered: %s (prio=%s)", inst.meta.name, inst.meta.priority)

    def _discover_local(self):
        logger.warning(f"🔍 Tentative de chargement depuis: {settings.plugin_package}")
        try:
            pkg = importlib.import_module(settings.plugin_package)
            for _, name, _ in pkgutil.iter_modules(pkg.__path__):
                module_path = f"{settings.plugin_package}.{name}"
                logger.info(f"📦 Découverte module: {module_path}")
                try:
                    m = importlib.import_module(module_path)
                    for obj in vars(m).values():
                        if inspect.isclass(obj) and issubclass(obj, BasePlugin) and obj is not BasePlugin:
                            self._register(obj())
                except Exception as e:
                    logger.error("❌ Échec du chargement du plugin %s: %s", module_path, e)
        except ModuleNotFoundError:
            logger.warning("⚠️ Plugin package '%s' introuvable", settings.plugin_package)

    def _discover_entrypoints(self):
        for ep in pkg_resources.iter_entry_points("perfectai_plugins"):
            try:
                mod = importlib.import_module(ep.module_name)
                for obj in vars(mod).values():
                    if inspect.isclass(obj) and issubclass(obj, BasePlugin) and obj is not BasePlugin:
                        self._register(obj())
            except Exception as e:
                logger.error("Failed loading entrypoint %s: %s", ep, e)

    @property
    def ordered(self) -> List[BasePlugin]:
        return sorted(self._plugins.values(), key=lambda p: p.meta.priority)

# —————————————————————————————————————————————————————————————————————
# Engine
# —————————————————————————————————————————————————————————————————————

class Engine:
    def __init__(self, manager: PluginManager):
        self.manager = manager
        self.semaphore = asyncio.BoundedSemaphore(settings.concurrency_limit)

    async def execute(self, payload: Dict[str, Any]) -> Context:
        ctx: Context = {"payload": payload, "ts_start": datetime.utcnow().isoformat()}
        async with self.semaphore:
            for plugin in self.manager.ordered:
                name = plugin.meta.name
                logger.info(f"🧩 Exécution plugin : {name}")
                start = time.time()
                try:
                    await plugin.before(ctx)
                    ctx = await plugin.run(ctx)
                    await plugin.after(ctx)
                except Exception as e:
                    PLUGIN_ERR.labels(plugin=name).inc()
                    ctx.setdefault("errors", []).append({"plugin": name, "error": str(e)})
                    logger.exception("Plugin %s failed", name)
                finally:
                    PLUGIN_LAT.labels(plugin=name).observe(time.time() - start)
        # Injecte la réponse du LLM dans ctx["response"]
        ctx["response"] = ctx.get("llm_response", "")
        ctx["ts_end"] = datetime.utcnow().isoformat()
        return ctx

# —————————————————————————————————————————————————————————————————————
# FastAPI app
# —————————————————————————————————————————————————————————————————————

pm     = PluginManager()
engine = Engine(pm)
app    = FastAPI(title=settings.app_name, version=settings.version)
app.add_middleware(CORSMiddleware, allow_origins=settings.cors_origins,
                   allow_methods=["*"], allow_headers=["*"])

@app.middleware("http")
async def metrics_middleware(request: Request, call_next):
    if settings.enable_metrics:
        REQ_COUNT.inc()
        with REQ_LAT.time():
            return await call_next(request)
    return await call_next(request)

@app.get("/healthz")
async def healthz():
    return {"status": "ok", "time": datetime.utcnow().isoformat()}

@app.get("/metrics")
async def metrics():
    if not settings.enable_metrics:
        raise HTTPException(status_code=404, detail="Metrics disabled")
    return Response(generate_latest(), media_type="text/plain")

class RunRequest(BaseModel):
    data: Dict[str, Any] = Field(default_factory=dict)

@app.post("/run")
async def run_endpoint(req: RunRequest, request: Request):
    if settings.master_key:
        token = request.headers.get("X-Master-Key", "")
        if token != settings.master_key:
            raise HTTPException(status_code=401, detail="Unauthorized")
    # Exécution
    ctx = await engine.execute(req.data)
    # On renvoie dans payload.response
    ctx["payload"]["response"] = ctx.get("response", "")
    return ctx

@app.websocket("/ws")
async def websocket_endpoint(ws: WebSocket):
    await ws.accept()
    try:
        while True:
            data = await ws.receive_json()
            out  = await engine.execute(data)
            await ws.send_json(out)
    except WebSocketDisconnect:
        logger.info("WebSocket disconnected")

# —————————————————————————————————————————————————————————————————————
# CLI
# —————————————————————————————————————————————————————————————————————

async def repl():
    print(f"🛠 {settings.app_name} v{settings.version} CLI. Type exit to quit.")
    while True:
        txt = input("> ")
        if txt.lower() in ("exit", "quit"):
            break
        ctx = await engine.execute({"message": txt})
        print(ctx)

def main():
    parser = argparse.ArgumentParser(description=settings.app_name)
    parser.add_argument("--serve", action="store_true", help="Run REST & WS server")
    parser.add_argument("--cli",   action="store_true", help="Run interactive CLI")
    parser.add_argument("--host",  default=settings.host)
    parser.add_argument("--port",  type=int, default=settings.port)
    args = parser.parse_args()
    if args.serve:
        uvicorn.run(app, host=args.host, port=args.port, reload=settings.debug)
    elif args.cli:
        asyncio.run(repl())
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
