# launcher.py

import os
from dotenv import load_dotenv

load_dotenv()  # ✅ Charge les variables depuis .env

if __name__ == "__main__":
    print("🧠 Lancement de PerfectAI Core...")
    os.system("uvicorn noyau_core:app --host 0.0.0.0 --port 8000 --reload")
