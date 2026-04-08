# 🤖 Buddy AI — Your Sarcastic AI Best Friend

> *"Like JARVIS, but with actual personality and zero corporate energy."*

Buddy AI is an open-source, modular AI assistant that actually feels like talking to a friend — a really smart, slightly savage, but ultimately loyal one. It searches the web, runs system commands, remembers your conversations, and does it all while roasting you just the right amount.

## Features

- **Personality Engine** — Four mood modes: `funny`, `serious`, `savage`, `chill`
- **Real-time Web Search** — DuckDuckGo + SerpAPI fallback, no hallucinations
- **System Commands** — Open apps, files, run shell commands
- **Conversation Memory** — Remembers context within sessions
- **Plugin System** — Drop-in plugin architecture for extending capabilities
- **Voice I/O** — Speech recognition + text-to-speech (optional)
- **Custom Wake Name** — Call it whatever you want
- **Dual Interface** — CLI terminal mode + React web UI
- **Debug/Logging** — Full logging with debug mode

## Architecture

```
buddy-ai/
├── main.py                 # Entry point & orchestrator
├── config.py               # All configuration
├── requirements.txt        # Python dependencies
├── core/
│   ├── __init__.py
│   ├── brain.py            # LLM interface (OpenAI / Ollama / LiteLLM)
│   └── orchestrator.py     # Routes queries to the right module
├── personality/
│   ├── __init__.py
│   ├── engine.py           # Humor/tone transformation layer
│   └── prompts.py          # System prompts for each mood
├── memory/
│   ├── __init__.py
│   └── context.py          # Short-term conversation memory
├── tools/
│   ├── __init__.py
│   ├── search.py           # Web search (DuckDuckGo + SerpAPI)
│   ├── system_cmd.py       # System commands (open apps, files)
│   └── summarizer.py       # Summarize search results
├── plugins/
│   ├── __init__.py
│   ├── loader.py           # Plugin discovery & loading
│   └── example_plugin.py   # Example plugin template
├── frontend/
│   └── index.html          # React web UI (single-file)
├── tests/
│   └── test_core.py        # Unit tests
├── logs/                   # Log output directory
└── docs/
    └── SETUP.md            # Detailed setup guide
```

## Quick Start

```bash
# 1. Clone the repo
git clone https://github.com/yourusername/buddy-ai.git
cd buddy-ai

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set up your .env file
cp .env.example .env
# Edit .env with your API keys (or use Ollama for free local LLM)

# 5. Run it
python main.py
```

## Configuration

Edit `config.py` or set environment variables:

| Variable | Default | Description |
|----------|---------|-------------|
| `BUDDY_NAME` | `Buddy` | What you call the assistant |
| `USER_NAME` | `Boss` | What it calls you |
| `MOOD` | `funny` | Default mood: funny/serious/savage/chill |
| `LLM_PROVIDER` | `ollama` | LLM backend: openai/ollama/litellm |
| `LLM_MODEL` | `llama3` | Model name |
| `OPENAI_API_KEY` | — | Required only if using OpenAI |
| `SERPAPI_KEY` | — | Optional, for SerpAPI search |
| `VOICE_ENABLED` | `false` | Enable voice input/output |
| `DEBUG` | `false` | Enable debug logging |

## Mood Modes

- **Funny** 😄 — Default. Witty, jokey, meme-aware
- **Serious** 🧠 — Drops the act, gives you straight answers
- **Savage** 🔥 — Maximum roast energy, still helpful
- **Chill** 😎 — Relaxed, laid-back, surfer vibes

Switch anytime: type `!mood savage` in chat.

## LLM Options

| Provider | Cost | Setup |
|----------|------|-------|
| **Ollama** (recommended) | Free | `ollama pull llama3` |
| **OpenAI** | Paid | Set `OPENAI_API_KEY` |
| **LiteLLM** | Varies | Supports 100+ providers |

## Plugin System

Drop a Python file in `plugins/` with this structure:

```python
PLUGIN_NAME = "my_plugin"
PLUGIN_DESCRIPTION = "Does something cool"
PLUGIN_COMMANDS = ["!mycommand"]

def handle(command: str, args: str) -> str:
    return "Plugin response here"
```

It auto-loads on startup.

## License

MIT — do whatever you want with it.

## Contributing

PRs welcome. Keep the vibe alive. No corporate energy allowed.
