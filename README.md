# 18th Century English Slang Dictionary

This project is a web application for exploring and searching 18th century English slang words. It features:

- A main page with an alphabetical list of slang words, divided by letter
- Each word links to a dedicated page with its definition
- A search function for finding words
- An About Us page describing the project

## Tech Stack
- Frontend: HTML, CSS
- Backend: Python (Flask)

## Setup
1. Install dependencies:
   ```
pip install -r requirements.txt
   ```
2. Run the app:
   ```
python app.py
   ```
3. Open your browser at http://127.0.0.1:5000/

## Folder Structure
- `app.py` — Flask backend
- `templates/` — HTML templates
- `static/` — CSS files
- `.github/` — Copilot instructions

## Note
- If you change the database model (add/remove fields), delete `instance/slang.db` and restart the app to recreate the database. This will erase all existing words.
