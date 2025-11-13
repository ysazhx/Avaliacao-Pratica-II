## Quick orientation

This is a small Flask + SQLite app that lists and registers "aluno" (students).

- Entry point: `app.py` (runs Flask dev server with `app.run(debug=True)`).
- DB: `fabrica.db` (path set via `PATH = 'fabrica.db'` in `app.py`). The DB schema is created by `start_db()` which executes `schema.sql` on startup.
- Templates: `templates/index.html`, `templates/cadastro.html` (Jinja2). Static CSS in `static/style.css`.

## Architecture & data flow (concise)

- On run: `start_db()` reads `schema.sql` and creates `fabrica.db` (if missing). Then Flask server starts.
- Routes:
  - `/` (index) — reads all rows from `aluno` and renders `templates/index.html`.
  - `/add` (cadastro) — GET shows the form, POST reads `request.form['nome']`, `['idade']`, `['curso']`, inserts them into `aluno`, commits and redirects to `index`.
- DB access pattern: use `get_db()` which returns an sqlite3.Connection with `row_factory = sqlite3.Row`. Example usage in `app.py`:

  db = get_db()
  db.execute('INSERT INTO aluno (nome, idade, curso) VALUES (?, ?, ?)', (nome, idade, curso))
  db.commit(); db.close()

## Important repository-specific details you must know

- Schema file: `schema.sql` — defines table `aluno` with columns `id`, `nome`, `idade`, `curso`.
  - Note: `schema.sql` currently contains `id INTERGER PRIMARY KEY AUTOINCREMENT` (typo INTERGER). SQLite is permissive about type names, but if you intend strict SQL compatibility, correct to `INTEGER`.
- DB lifecycle: `start_db()` runs automatically when `app.py` is executed as `__main__`. To re-create the DB after changing `schema.sql`, stop the server, delete `fabrica.db`, then re-run `python app.py`.
- Templates refer to endpoints by name. Example: `index.html` uses `{{ url_for('cadastro') }}` — keep route function names stable when refactoring.
- Form field names are the authoritative keys: `nome`, `idade`, `curso`. Use the same keys when adding features that read POSTed form data.

## Common tasks & exact commands (Windows PowerShell)

- Start development server (creates DB if missing):

  python app.py

- Recreate DB after schema change:

  Remove `fabrica.db` then run `python app.py` (or stop/restart the server). The app runs `start_db()` on startup which executes `schema.sql`.

## Conventions and patterns to follow when contributing

- Use `get_db()` for all DB interactions (keeps `row_factory` consistent for templates).
- Close DB after commits: call `db.commit()` then `db.close()` as currently done in `app.py`.
- Keep Jinja templates minimal and use `url_for('<endpoint_name>')` for links. Examples: `url_for('index')`, `url_for('cadastro')`.
- Avoid committing `fabrica.db` to source control (it's generated; add to .gitignore if not already ignored).

## Where to look for examples when implementing features

- Adding a new record: follow `/add` handler in `app.py` and `templates/cadastro.html` for form structure and POST keys.
- Displaying records: follow `/` handler and `index.html` — uses `alunos = db.execute('SELECT * FROM aluno').fetchall()` and Jinja loop `{% for aluno in alunos %}`.

## Integration & risk notes

- No external services or packages besides Python standard library + Flask and sqlite3 are used in the repo. If adding dependencies, include a `requirements.txt` with pinned versions.
- The app runs in Flask debug mode by default — do not assume this is production-ready. If you add long-running operations, move them off the request thread.

## What I (the agent) should do when asked to modify/extend the project

- Inspect `app.py`, `schema.sql`, templates and static files first.
- If adding DB changes: update `schema.sql` and document the migration step; instruct to delete `fabrica.db` and restart to apply schema changes.
- Keep route names and form field names unchanged unless updating templates and any code referencing them.

---

If anything here is incomplete or you'd like examples for adding specific routes, tests, or a `requirements.txt`, tell me which area to expand.
