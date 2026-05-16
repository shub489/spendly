# Spec: Registration

## Overview
Wire up the registration form so new users can create an account. The GET route and
`register.html` template already exist; this step adds the POST handler, a
`create_user()` DB helper, basic server-side validation, and shown a success message and  redirect to the
login page on success. No session is started here — authentication is handled in a
later step.

## Depends on
Step 01 — Database Setup (users table and `get_db()` must exist).

## Routes
- `POST /register` — validate form fields, insert user, redirect to `/login` on
  success or re-render with an error message — public

## Database changes
No new tables or columns. One new helper function in `database/db.py`:

- `create_user(name, email, password_hash)` — inserts a row into `users` and
  returns the new `id`. Raises `sqlite3.IntegrityError` if email is already taken.

## Templates
- **Modify:** `templates/register.html`
  - Change hardcoded `action="/register"` → `action="{{ url_for('register') }}"`
  - Ensure the `{% if error %}` block is already present (it is — no change needed)
  - Re-populate `name` and `email` fields with submitted values on validation
    failure so the user doesn't retype them

## Files to change
- `database/db.py` — add `create_user()`
- `app.py` — add `POST` to the `/register` route; import `redirect`, `url_for`,
  `request` from flask; import `create_user` from `database.db`; add `secret_key`
  to the Flask app
- `templates/register.html` — fix hardcoded action URL; re-populate fields on error

## Files to create
- `static/css/auth.css` — styles for `.auth-section`, `.auth-container`,
  `.auth-header`, `.auth-title`, `.auth-subtitle`, `.auth-card`, `.auth-error`,
  `.form-group`, `.form-input`, `.btn-submit`, `.auth-switch`. These classes are
  already referenced in the template but the stylesheet does not yet exist.

## New dependencies
No new dependencies.

## Rules for implementation
- No SQLAlchemy or ORMs — raw `sqlite3` only
- Parameterised queries only — no f-strings in SQL
- Passwords hashed with `werkzeug.security.generate_password_hash` before insert
- Use CSS variables — never hardcode hex values in `auth.css`
- All templates extend `base.html`
- Never put DB logic inside the route function — use `create_user()` in `db.py`
- Validate server-side before touching the DB:
  - name, email, password are all required (non-empty after strip)
  - password must be at least 8 characters
- On duplicate email, catch `sqlite3.IntegrityError` and show a friendly error —
  do not let a 500 bubble to the user
- On success, `redirect(url_for('login'))` — do not render a template
- `app.secret_key` must be set (needed for future session use); use a fixed dev
  string for now, e.g. `app.secret_key = "dev-secret-change-in-prod"`

## Definition of done
- [ ] Visiting `/register` (GET) still renders the form without errors
- [ ] Submitting the form with all valid fields creates a user in `users` table
- [ ] On success, the browser is redirected to `/login`
- [ ] Submitting with a blank name, email, or password shows an inline error and
      re-renders the form (no redirect)
- [ ] Submitting with a password shorter than 8 characters shows a validation error
- [ ] Submitting with an already-registered email shows "Email already in use" error
- [ ] On validation failure, name and email fields are pre-filled with the submitted
      values; password field is cleared
- [ ] Password is stored as a hash — the plain-text password never reaches the DB
- [ ] `auth.css` is linked in `base.html` or `register.html` and the page is styled
- [ ] No hardcoded URLs in templates — all internal links use `url_for()`
