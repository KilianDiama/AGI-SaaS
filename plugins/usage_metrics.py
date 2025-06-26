# plugins/usage_metrics.py
import logging
from prometheus_client import Counter
from noyau_core import BasePlugin, Context, Meta

logger = logging.getLogger("plugin.usage_metrics")
REQ_BY_PLUGIN = Counter("pai_requests_by_plugin", "Nb appels par plugin", ["plugin"])

class UsageMetricsPlugin(BasePlugin):
    meta = Meta(name="usage_metrics", priority=-930, version="1.0", author="Matt")

    async def before(self, ctx: Context) -> None:
        # nothing
        pass

    async def run(self, ctx: Context) -> Context:
        # on incrémente pour chaque cycle
        for name in ctx.get("plugins_log", []):
            plugin = name.split()[0]
            REQ_BY_PLUGIN.labels(plugin=plugin).inc()
        return ctx
