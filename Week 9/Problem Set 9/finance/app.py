import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    user_id = session["user_id"]

    # Fetch user's cash
    cash = db.execute("SELECT cash FROM users WHERE id = ?", user_id)[0]["cash"]

    # Fetch user's current holdings
    rows = db.execute("SELECT symbol, shares FROM holdings WHERE user_id = ?", user_id)

    holdings = []
    total = cash

    for row in rows:
        quote = lookup(row["symbol"])
        if quote:
            total_stock = row["shares"] * quote["price"]
            holdings.append({
                "symbol": row["symbol"],
                "name": quote["name"],
                "shares": row["shares"],
                "price": quote["price"],
                "total": total_stock
            })
            total += total_stock

    return render_template("index.html", holdings=holdings, cash=cash, grand_total=total)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "POST":
        symbol = request.form.get("symbol")
        shares = request.form.get("shares")

        if not symbol:
            return apology("must provide symbol")

        if not shares or not shares.isdigit() or int(shares) <= 0:
            return apology("invalid number of shares")

        quote = lookup(symbol.upper())
        if not quote:
            return apology("invalid symbol")

        price = quote["price"]
        cost = price * int(shares)

        user_id = session["user_id"]
        cash = db.execute("SELECT cash FROM users WHERE id = ?", user_id)[0]["cash"]

        if cash < cost:
            return apology("can't afford")

        db.execute("UPDATE users SET cash = cash - ? WHERE id = ?", cost, user_id)

        db.execute("INSERT INTO transactions (user_id, symbol, name, shares, price, type) VALUES (?, ?, ?, ?, ?, ?)",
                   user_id, quote["symbol"], quote["name"], int(shares), quote["price"], "BUY")

        db.execute("INSERT INTO holdings (user_id, symbol, name, shares) VALUES (?, ?, ?, ?) ON CONFLICT(symbol, user_id) DO UPDATE SET shares = shares + excluded.shares",
                   user_id, quote["symbol"], quote["name"], int(shares))

        flash("Bought!")
        return redirect("/")

    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    user_id = session["user_id"]
    rows = db.execute(
        "SELECT symbol, shares, price, timestamp FROM transactions WHERE user_id = ? ORDER BY timestamp DESC", user_id)
    return render_template("history.html", transactions=rows)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""
    session.clear()

    if request.method == "POST":
        if not request.form.get("username"):
            return apology("must provide username", 403)

        elif not request.form.get("password"):
            return apology("must provide password", 403)

        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        session["user_id"] = rows[0]["id"]

        return redirect("/")

    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""
    session.clear()
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    if request.method == "POST":
        symbol = request.form.get("symbol")

        if not symbol:
            return apology("must provide symbol", 400)

        quote = lookup(symbol.upper())

        # Check if quote is None or missing price
        if not quote or "price" not in quote:
            return apology("invalid symbol or API error", 400)

        return render_template("quoted.html", name=quote["name"], symbol=quote["symbol"], price=quote["price"])

    return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        if not username or not password or not confirmation:
            return apology("must fill all fields")

        if password != confirmation:
            return apology("passwords don't match")

        hash_pass = generate_password_hash(password)

        try:
            db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", username, hash_pass)
        except:
            return apology("username already taken")

        user_id = db.execute("SELECT id FROM users WHERE username = ?", username)[0]["id"]
        session["user_id"] = user_id

        return redirect("/")

    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    user_id = session["user_id"]
    if request.method == "POST":
        symbol = request.form.get("symbol")
        shares = request.form.get("shares")

        if not symbol or not shares or not shares.isdigit() or int(shares) <= 0:
            return apology("invalid input")

        owned = db.execute(
            "SELECT shares FROM holdings WHERE user_id = ? AND symbol = ?", user_id, symbol.upper())

        if not owned or owned[0]["shares"] < int(shares):
            return apology("too many shares")

        quote = lookup(symbol.upper())
        price = quote["price"]
        revenue = int(shares) * price

        db.execute("UPDATE users SET cash = cash + ? WHERE id = ?", revenue, user_id)

        db.execute("INSERT INTO transactions (user_id, symbol, shares, price, type) VALUES (?, ?, ?, ?, ?)",
                   user_id, symbol.upper(), -int(shares), price, "SELL")

        db.execute("UPDATE holdings SET shares = shares - ? WHERE user_id = ? AND symbol = ?",
                   int(shares), user_id, symbol.upper())

        db.execute("DELETE FROM holdings WHERE shares <= 0")

        flash("Sold!")
        return redirect("/")

    else:
        symbols = db.execute("SELECT symbol FROM holdings WHERE user_id = ?", user_id)
        return render_template("sell.html", symbols=symbols)
