# Spec: Backend Routes for Profile Page

## Overview
This step wires the `/profile` route to real database data, replacing every hardcoded dict in `app.py` with live queries against the `users` and `expenses` tables. Four new helper functions are added to `database/db.py`: one to fetch a user by their primary key, one to list their most recent expenses, one to compute summary stats (total spent, transaction count, top category), and one to produce a per-category breakdown with totals and percentages. The `profile.html` template requires no structural changes — only the context variables it already expects will now come from the database instead of Python literals.

## Depends on
- Step 1: Database setup (`users` and `expenses` tables must exist)
- Step 2: Registration (real user rows must be insertable)
- Step 3: Login + Logout (session must carry `user_id`)
- Step 4: Profile Page Design (template and route structure must already exist)

## Routes
No new routes. The existing `GET /profile` route is modified to use real DB queries instead of hardcoded data.

## Database changes
No database changes. The existing `users` and `expenses` tables are sufficient. All needed data (name, email, created_at, amount, category, date, description) is already present.

## Templates
- **Create:** None
- **Modify:** `templates/profile.html` — update `member_since` to display a formatted date string (e.g. "January 2026") derived from `users.created_at`; ensure `amount` values render with comma formatting (₹ with Indian number format)

## Files to change
- `database/db.py` — add four new helper functions:
  1. `get_user_by_id(user_id)` — `SELECT * FROM users WHERE id = ?`
  2. `get_expenses_by_user(user_id, limit=10)` — recent expenses ordered by `date DESC`, `created_at DESC`
  3. `get_expense_stats(user_id)` — returns dict with `total_spent` (SUM), `txn_count` (COUNT), `top_category` (category with highest SUM)
  4. `get_category_breakdown(user_id)` — returns list of dicts `{name, total, pct}` ordered by total DESC; `pct` is integer percentage of grand total
- `app.py` — replace all hardcoded context dicts in the `/profile` route with calls to the four new helpers; compute `initials` from `user["name"]`; format `member_since` from `user["created_at"]`

## Files to create
None.

## New dependencies
No new dependencies.

## Rules for implementation
- No SQLAlchemy or ORMs — use raw `sqlite3` via `get_db()` only
- Parameterised queries only — never use f-strings or string concatenation in SQL
- Passwords hashed with werkzeug (no auth changes in this step)
- Use CSS variables — never hardcode hex values
- All templates extend `base.html`
- `get_expense_stats` and `get_category_breakdown` must each open and close their own DB connection — no shared connection objects passed between helpers
- `pct` in category breakdown must be computed in Python, not SQL, to avoid division-by-zero when a user has no expenses
- `initials` must be derived from the first letter of each word in `user["name"]`, uppercased, max 2 characters
- `member_since` must be formatted as "Month YYYY" (e.g. "January 2026") using Python's `datetime.strptime` on `users.created_at`
- Amount display: pass raw float values from DB; format with `"{:,.0f}".format(amount)` in the route before passing to template (keeps template logic minimal)
- If a user has no expenses, the profile must still render — stats should show zeros and categories should be an empty list

## Definition of done
- [ ] Visiting `/profile` while logged in as the demo user shows "Demo User" and "demo@spendly.com" (pulled from DB, not hardcoded)
- [ ] The member-since date matches the demo user's `created_at` in the database
- [ ] The total spent stat matches the sum of all demo user expenses in the database (₹6,299)
- [ ] The transaction count matches the number of expense rows for the demo user (8)
- [ ] The top category shown is "Shopping" (highest total for demo user)
- [ ] All 8 demo transactions appear in the recent transactions table in date-descending order
- [ ] The category breakdown shows all 7 categories with correct totals and percentages that sum to 100%
- [ ] Registering a new user and visiting `/profile` shows that user's name/email with zero stats and an empty transaction list — no crash
- [ ] No hardcoded user/expense data remains in the `/profile` route function in `app.py`
- [ ] All SQL in `database/db.py` uses `?` placeholders — no f-strings in any query
