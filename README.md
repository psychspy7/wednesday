# WEDNESDAY — Experimental Personal AI Assistant

> A modular local-first AI assistant prototype with personality, search, voice experiments, and a web interface.

WEDNESDAY is an experimental Python assistant project exploring conversational AI, local model support, web search, voice I/O, memory, and personality-driven responses.

## Status

**Prototype / refactor in progress.**

The current public snapshot contains a mixture of legacy flat modules and newer package-oriented code. Some entry-point imports still reference modules that are not yet present in this repository, so the project should not currently be treated as a one-command production install.

This README intentionally reflects the real state of the code instead of advertising unsupported setup steps.

## Current files

```text
wednesday/
├── main.py
├── web_server.py
├── config.py
├── engine.py
├── prompts.py
├── search.py
├── summarizer.py
├── requirements.txt
├── .env.example
├── .gitignore
├── LICENSE
└── README.md
```

## Intended capabilities

- Multiple personality modes
- Local LLM support through Ollama
- Optional OpenAI/LiteLLM providers
- Web search and summarization
- Session memory
- Voice input/output experiments
- CLI and browser-based interfaces
- Environment-based configuration

## Configuration

Copy the example environment file and fill in only the services you actually use:

```bash
cp .env.example .env
```

Never commit the resulting `.env` file or any real API keys. The repository's `.gitignore` already excludes `.env`, logs, virtual environments, Python cache files, IDE metadata, and build output.

## Development roadmap

Before calling the project stable, the next cleanup should:

1. Consolidate the flat modules into one consistent package structure.
2. Restore or rewrite the missing orchestrator layer referenced by `main.py` and `web_server.py`.
3. Add a minimal automated test suite.
4. Verify CLI startup from a fresh clone.
5. Verify web startup from a fresh clone.
6. Pin and review dependencies.

## Security

- API keys belong in environment variables only.
- Do not expose local system-command features to untrusted remote users.
- Keep any web/API server bound to localhost unless authentication and authorization are deliberately added.
- Review dependencies before using the project on a sensitive machine.

## License

MIT
