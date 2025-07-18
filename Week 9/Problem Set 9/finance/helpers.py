import requests
import urllib.parse
from flask import redirect, render_template, session
from functools import wraps

def apology(message, code=400):
    return render_template("apology.html", top=code, bottom=message), code

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

def lookup(symbol):
    try:
        api_key = "YSZTQ868AED6D5PK"
        url = f"https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={urllib.parse.quote(symbol)}&interval=5min&apikey={api_key}"
        response = requests.get(url)
        data = response.json()
        price = float(list(data["Time Series (5min)"].values())[0]["4. close"])
        return {
            "symbol": symbol.upper(),
            "name": symbol.upper(),  # Could replace with real name using another API
            "price": price
        }
    except Exception:
        return None

def usd(value):
    return f"${value:,.2f}"
