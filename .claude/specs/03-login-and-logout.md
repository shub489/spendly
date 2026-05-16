# Spec: Login and Logout

## Overview
Wire up the login and logout flows so users can authenticate and end their session.
`GET /login` already renders `login.html`; this step adds the `POST /login` handler
that verifies credentials against the database, writes the user's id and name into
Flask's signed session cookie, and redirects to the dashboard on success. The `GET
/logout` stub is replaced with a real handler that clears the session and redirects
to the landing page. `base.html`'s navigation is updated to conditionally show
"Hi, {name}" and a Logout link when a session exists, and Sign in / Get started
when it does not.

## Depends on
- Step 01 — Database Setup (`get_db()`, users table)
- Step 02 — Registration (`create_user()`, `app.secret_key` already set)

## Routes
- `POST /login` — validate credentials, set session, redirect to `/` — public
- `GET /logout` — clear session, redirect to `/` — any (no login required)

## Database changes
No new tables or columns. One new helper in `database/db.py`:

- `get_user_by_email(email)` — queries `users` WHERE email = ? and returns the
  matching `sqlite3.Row` (with `id`, `name`, `email`, `password_hash`), or `None`
  if not found. Uses a parameterized query.

## Templates
- **Modify:** `templates/login.html`
  - Change hardcoded `action="/login"` → `action="{{ url_for('login') }}"`
  - Re-populate the email field with the submitted value on error:
    `value="{{ email or '' }}"`
- **Modify:** `templates/base.html`
  - Replace the hardcoded "Sign in" / "Get started" nav links with a Jinja2
    conditional block:
    - If `session.user_id` is set: show "Hi, {{ session.user_name }}" (plain text)
      and a "Logout" link pointing to `url_for('logout')`
    - Otherwise: show "Sign in" → `url_for('login')` and "Get started" →
      `url_for('register')`

## Files to change
- `database/db.py` — add `get_user_by_email()`
- `app.py` — import `session`, `check_password_hash`; add POST to `/login`; replace
  `/logout` stub with real handler; import `get_user_by_email`
- `templates/login.html` — fix hardcoded action URL; re-populate email on error
- `templates/base.html` — session-aware nav conditional

## Files to create
None.

## New dependencies
No new dependencies. `werkzeug.security.check_password_hash` is already available
via the installed `werkzeug` package.

## Rules for implementation
- No SQLAlchemy or ORMs — raw `sqlite3` only
- Parameterised queries only — no f-strings in SQL
- Passwords verified with `werkzeug.security.check_password_hash` — never compare
  plain-text passwords
- Use CSS variables — never hardcode hex values
- All templates extend `base.html`
- No DB logic inside route functions — use `get_user_by_email()` in `db.py`
- Session keys must be exactly `user_id` (int) and `user_name` (str) — these are
  the keys `base.html` will check
- On login failure, show a single vague error ("Invalid email or password.") —
  never reveal whether the email exists
- On successful login: `session.clear()` then set both keys, then redirect — always
  clear before setting to avoid session fixation
- `GET /logout` must call `session.clear()` then `redirect(url_for('landing'))` —
  no template render

## Definition of done
- [ ] `GET /login` still renders the form with no errors
- [ ] Submitting correct email + password sets session and redirects to `/`
- [ ] After login, the nav shows "Hi, {name}" and a Logout link
- [ ] Submitting a wrong password shows "Invalid email or password." — form stays,
      email field is pre-filled
- [ ] Submitting a non-existent email shows the same vague error
- [ ] Submitting with blank email or password shows "All fields are required."
- [ ] Visiting `/logout` clears the session and redirects to `/`
- [ ] After logout, the nav shows "Sign in" and "Get started" again
- [ ] Nav links use `url_for()` — no hardcoded URLs in `base.html`
- [ ] The demo user (`demo@spendly.com` / `demo123`) can log in successfully
