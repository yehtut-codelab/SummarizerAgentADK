---
name: summarizer-agent-e2e
description: "Create SummarizerAgent end to end: scaffold project structure, implement ResearchAgent + SummarizerAgent, configure .env GOOGLE_API_KEY, add Chainlit app.py chat UI, update requirements/README, and provide run/test commands. Use when user asks: build SummarizerAgent, create app.py with Chainlit, or set up a GitHub-ready agent repo."
---

# SummarizerAgent End-to-End Skill

## Goal

Build a complete, runnable `SummarizerAgent` project from notebook-style code into a clean GitHub repo structure.

## Inputs To Confirm

- Target folder name (default: `SummarizerAgent`)
- Model name (default: `gemini-2.5-flash-lite`)
- UI mode:
  - Chainlit only
  - CLI + Chainlit (default)
- Python version target (recommend `3.11` or `3.12` on Windows)

## Expected Output Structure

```text
SummarizerAgent/
  app.py
  .env.example
  .gitignore
  README.md
  requirements.txt
  src/
    summarizer_agent/
      __init__.py
      config.py
      agents.py
      main.py
  tests/
    test_agents.py
```

## Implementation Steps

1. Create folder structure.
2. Add `config.py` with:
   - dotenv loading
   - retry options
   - `GOOGLE_API_KEY` validation
3. Add `agents.py` with only:
   - `ResearchAgent`
   - `SummarizerAgent`
4. Add `main.py` with:
   - async run function
   - response-text extraction from event outputs
   - Windows-safe loop shutdown for CLI execution
5. Add `app.py` with Chainlit handlers:
   - `on_chat_start`
   - `on_message` that calls the agent run function
6. Add `requirements.txt` (minimum):
   - `google-adk`
   - `google-genai`
   - `python-dotenv`
   - `chainlit`
   - `pytest`
7. Add `.env.example` with `GOOGLE_API_KEY=`.
8. Add `.gitignore` for Python/venv/env artifacts.
9. Add `README.md` with setup, run, and troubleshooting.
10. Add basic test that validates both agents instantiate.

## Validation Checklist

- `app.py` sends only response text back to user.
- `GOOGLE_API_KEY` is read from `.env` or environment.
- README includes both commands:
  - `python -m src.summarizer_agent.main`
  - `chainlit run app.py -w`
- No `kaggle_secrets` references.
- Imports resolve after dependencies are installed.

## Windows Notes

If users report asyncio SSL shutdown traces (`Fatal error on SSL transport`), prefer:
- Python `3.11` or `3.12`
- Selector event loop policy and graceful loop teardown in CLI wrapper

## Done Criteria

- Project runs in CLI mode and returns summarized output.
- Project runs in Chainlit mode and answers user messages.
- Repo is ready to push to GitHub with documentation and reproducible setup.
