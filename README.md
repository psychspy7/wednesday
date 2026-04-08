# wednesday
Ai Assistant
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
