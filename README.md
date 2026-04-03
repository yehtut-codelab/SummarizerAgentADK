# SummarizerAgent

This project contains only:
- `ResearchAgent`
- `SummarizerAgent`

It supports two run modes:
- CLI mode (`python -m src.summarizer_agent.main`)
- Chat UI mode with Chainlit (`chainlit run app.py -w`)

## Project Structure

```text
SummarizerAgent/
  app.py
  .env.example
  .gitignore
  LICENSE
  requirements.txt
  README.md
  src/
    summarizer_agent/
      __init__.py
      config.py
      agents.py
      main.py
  tests/
    test_agents.py
```

## Setup

1. Use Python 3.11 or 3.12 (recommended for stable asyncio behavior on Windows).
2. Create and activate a virtual environment.
3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Create a `.env` file from `.env.example` and add your key:

```env
GOOGLE_API_KEY=your_google_api_key
```

## Run (CLI)

```bash
python -m src.summarizer_agent.main
```

Then enter a prompt when asked.

## Run (Chainlit Chat UI)

```bash
chainlit run app.py -w
```

Then open the local URL shown in terminal (usually http://localhost:8000).

## Run Tests

```bash
pytest -q
```

## Prepare For GitHub Upload

1. Keep secrets out of git (`.env` is ignored, only `.env.example` is committed).
2. Ensure local runtime folders are not tracked (`.venv/`, `.chainlit/`, `.files/`, `__pycache__/`).
3. Commit the project files:

```bash
git add .
git commit -m "Prepare SummarizerAgent for GitHub"
```

4. Push to your repository:

```bash
git remote add origin <your-repo-url>
git branch -M main
git push -u origin main
```
