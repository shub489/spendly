import sqlite3
from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
from database.db import get_db, init_db, seed_db, create_user, get_user_by_email

app = Flask(__name__)
app.secret_key = "dev-secret-change-in-prod"

with app.app_context():
    init_db()
    seed_db()


# ------------------------------------------------------------------ #
# Routes                                                              #
# ------------------------------------------------------------------ #

@app.route("/")
def landing():
    return render_template("landing.html")


@app.route("/terms")
def terms():
    return render_template("terms.html")


@app.route("/privacy")
def privacy():
    return render_template("privacy.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if session.get("user_id"):
        return redirect(url_for("landing"))
    if request.method == "GET":
        return render_template("register.html")

    name     = request.form.get("name", "").strip()
    email    = request.form.get("email", "").strip()
    password = request.form.get("password", "")

    error = None
    if not name or not email or not password:
        error = "All fields are required."
    elif len(password) < 8:
        error = "Password must be at least 8 characters."

    if error:
        return render_template("register.html", error=error, name=name, email=email)

    try:
        create_user(name, email, generate_password_hash(password))
    except sqlite3.IntegrityError:
        return render_template(
            "register.html",
            error="An account with that email already exists.",
            name=name,
            email=email,
        )

    return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if session.get("user_id"):
        return redirect(url_for("landing"))
    if request.method == "GET":
        return render_template("login.html")

    email    = request.form.get("email", "").strip()
    password = request.form.get("password", "")

    if not email or not password:
        return render_template("login.html",
                               error="All fields are required.",
                               email=email)

    user = get_user_by_email(email)
    if user is None or not check_password_hash(user["password_hash"], password):
        return render_template("login.html",
                               error="Invalid email or password.",
                               email=email)

    session.clear()
    session["user_id"]   = user["id"]
    session["user_name"] = user["name"]
    return redirect(url_for("landing"))


# ------------------------------------------------------------------ #
# Placeholder routes — students will implement these                  #
# ------------------------------------------------------------------ #

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("landing"))


@app.route("/profile")
def profile():
    if not session.get("user_id"):
        return redirect(url_for("login"))

    user = {
        "name": "Demo User",
        "email": "demo@spendly.com",
        "initials": "DU",
        "member_since": "January 2026",
    }
    stats = {
        "total_spent": "6,299",
        "txn_count": 8,
        "top_category": "Shopping",
    }
    transactions = [
        {"date": "2026-05-18", "description": "Parking charges — monthly", "category": "Other", "amount": "250"},
        {"date": "2026-05-15", "description": "Shoes from Myntra", "category": "Shopping", "amount": "2,500"},
        {"date": "2026-05-12", "description": "Netflix subscription", "category": "Entertainment", "amount": "799"},
        {"date": "2026-05-10", "description": "Pharmacy — vitamins", "category": "Health", "amount": "600"},
        {"date": "2026-05-07", "description": "Electricity bill", "category": "Bills", "amount": "1,200"},
        {"date": "2026-05-05", "description": "Weekly grocery run", "category": "Food", "amount": "420"},
        {"date": "2026-05-03", "description": "Ola cab to office", "category": "Transport", "amount": "350"},
        {"date": "2026-05-01", "description": "Morning breakfast at cafe", "category": "Food", "amount": "180"},
    ]
    categories = [
        {"name": "Shopping", "total": "2,500", "pct": 40},
        {"name": "Bills", "total": "1,200", "pct": 19},
        {"name": "Entertainment", "total": "799", "pct": 13},
        {"name": "Health", "total": "600", "pct": 10},
        {"name": "Food", "total": "600", "pct": 9},
        {"name": "Transport", "total": "350", "pct": 6},
        {"name": "Other", "total": "250", "pct": 3},
    ]
    return render_template("profile.html", user=user, stats=stats,
                           transactions=transactions, categories=categories)


@app.route("/expenses/add")
def add_expense():
    return "Add expense — coming in Step 7"


@app.route("/expenses/<int:id>/edit")
def edit_expense(id):
    return "Edit expense — coming in Step 8"


@app.route("/expenses/<int:id>/delete")
def delete_expense(id):
    return "Delete expense — coming in Step 9"


if __name__ == "__main__":
    app.run(debug=True, port=5001)
