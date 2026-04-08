"""
config.py — Central configuration for Buddy AI.

All settings can be overridden via environment variables or a .env file.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env file if it exists
load_dotenv()

# ─── Paths ───────────────────────────────────────────────────────────────────
BASE_DIR = Path(__file__).parent.resolve()
LOG_DIR = BASE_DIR / "logs"
PLUGIN_DIR = BASE_DIR / "plugins"
LOG_DIR.mkdir(exist_ok=True)

# ─── Identity ────────────────────────────────────────────────────────────────
BUDDY_NAME = os.getenv("BUDDY_NAME", "Buddy")
USER_NAME = os.getenv("USER_NAME", "Boss")

# ─── Mood ─────────────────────────────────────────────────────────────────────
# Options: "funny", "serious", "savage", "chill"
DEFAULT_MOOD = os.getenv("MOOD", "funny")

# ─── LLM Provider ────────────────────────────────────────────────────────────
# Options: "openai", "ollama", "litellm"
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "ollama")
LLM_MODEL = os.getenv("LLM_MODEL", "llama3")

# OpenAI-specific
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")

# Ollama-specific
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")

# LLM parameters
LLM_TEMPERATURE = float(os.getenv("LLM_TEMPERATURE", "0.8"))
LLM_MAX_TOKENS = int(os.getenv("LLM_MAX_TOKENS", "1024"))

# ─── Search ───────────────────────────────────────────────────────────────────
SERPAPI_KEY = os.getenv("SERPAPI_KEY", "")
# If no SerpAPI key, we use DuckDuckGo (free, no key needed)

# ─── Voice ────────────────────────────────────────────────────────────────────
VOICE_ENABLED = os.getenv("VOICE_ENABLED", "false").lower() == "true"
TTS_ENGINE = os.getenv("TTS_ENGINE", "pyttsx3")  # "pyttsx3" or "gtts"

# ─── Memory ───────────────────────────────────────────────────────────────────
MAX_MEMORY_TURNS = int(os.getenv("MAX_MEMORY_TURNS", "20"))

# ─── Debug ────────────────────────────────────────────────────────────────────
DEBUG = os.getenv("DEBUG", "false").lower() == "true"
LOG_LEVEL = os.getenv("LOG_LEVEL", "DEBUG" if DEBUG else "INFO")

# ─── Web Server (for React frontend) ─────────────────────────────────────────
WEB_HOST = os.getenv("WEB_HOST", "127.0.0.1")
WEB_PORT = int(os.getenv("WEB_PORT", "8642"))
