# Taskflow (Flask + SQLite)

Rekurzív feladatkezelő webalkalmazás (hierarchia: 2.4.5 formátum), gyors rögzítéssel és felhasználói alapértelmezésekkel.

## Fejlesztői setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export FLASK_APP=run.py
flask run
