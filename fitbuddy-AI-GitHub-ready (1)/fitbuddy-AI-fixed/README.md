# FitBuddy AI

A small fitness-plan web app built with FastAPI, Jinja2 templates, SQLite, and Google's Gemini API.

## Features

- Collects user details and fitness preferences.
- Generates a 7-day workout plan using Gemini when an API key is configured.
- Uses a built-in demo plan if Gemini is not configured or returns no text.
- Generates a general nutrition/recovery tip.
- Saves user and plan records in SQLite.
- Includes a basic admin page for viewing and deleting users.

## Requirements

- Python 3.10 or newer
- pip
- Optional: a Google Gemini API key

## Run on Windows (PowerShell)

Open a terminal in the project root (the folder containing `requirements.txt`).

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
Copy-Item .env.example .env
```

Edit `.env` and set `GEMINI_API_KEY` if you want Gemini-generated results. Set `ADMIN_TOKEN` to a long, private value before using the admin page. Do not commit `.env` or share API keys.

Start the app from the project root:

```powershell
python -m uvicorn app.main:app --reload
```

Open http://127.0.0.1:8000

Health check: http://127.0.0.1:8000/api/health

## Project structure

```text
app/
  ai/
    gemini_client.py
    gemini_flash_generator.py
    gemini_generator.py
    updated_plan.py
  config.py
  database.py
  main.py
  routes.py
  schemas.py
static/
  style.css
templates/
  admin_login.html
  all_users.html
  index.html
  result.html
.env.example
.gitignore
requirements.txt
README.md
```

## Notes

- The SQLite database file is created locally when the app starts; it is intentionally not included in this source archive.
- `.venv`, `venv`, Python cache files, local databases, and `.env` are excluded by `.gitignore`.
- This is a starter/demo project. Review authentication, privacy, and safety before deploying it publicly.
- Fitness guidance is general information, not medical advice. Users should adapt activity to their circumstances and seek qualified guidance when needed.
