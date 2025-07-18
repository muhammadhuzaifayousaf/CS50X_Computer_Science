import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, url_for, session

# Configure application
app = Flask(__name__)
app.secret_key = "390d56583570f29cc254f6a851a87510"

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///birthdays.db")

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Get form data
        name = request.form.get("name").strip()
        month = request.form.get("month")
        day = request.form.get("day")

        # Validate input
        if not name or not month or not day:
            flash("All fields are required!")
            return redirect("/")

        try:
            month = int(month)
            day = int(day)
        except ValueError:
            flash("Month and Day must be numbers!")
            return redirect("/")

        if not (1 <= month <= 12):
            flash("Month must be between 1 and 12.")
            return redirect("/")
        if not (1 <= day <= 31):
            flash("Day must be between 1 and 31.")
            return redirect("/")

        # ❗ Prevent duplicates
        existing = db.execute("SELECT * FROM birthdays WHERE LOWER(name) = LOWER(?)", name)
        if existing:
            flash("That name is already in the list! Write full name.")
            return redirect("/")

        # Insert into database
        db.execute("INSERT INTO birthdays (name, month, day) VALUES (?, ?, ?)", name, month, day)
        flash("Birthday added successfully!")
        return redirect("/")

    else:
        # Show all birthdays
        birthdays = db.execute("SELECT * FROM birthdays")
        return render_template("index.html", birthdays=birthdays)


@app.route("/delete", methods=["POST"])
def delete():
    birthday_id = request.form.get("id")
    if birthday_id:
        db.execute("DELETE FROM birthdays WHERE id = ?", birthday_id)
        flash("Birthday deleted successfully!")
    else:
        flash("Failed to delete birthday.")
    return redirect("/")


@app.route("/edit", methods=["POST"])
def edit():
    birthday_id = request.form.get("id")
    name = request.form.get("name")
    month = request.form.get("month")
    day = request.form.get("day")

    # Basic validation
    if not birthday_id or not name or not month or not day:
        flash("All fields are required for editing.")
        return redirect("/")

    try:
        month = int(month)
        day = int(day)
    except ValueError:
        flash("Month and Day must be numbers.")
        return redirect("/")

    if not (1 <= month <= 12) or not (1 <= day <= 31):
        flash("Invalid date.")
        return redirect("/")

    # Update the birthday entry
    db.execute("UPDATE birthdays SET name = ?, month = ?, day = ? WHERE id = ?", name, month, day, birthday_id)
    flash("Birthday updated successfully!")
    return redirect("/")
