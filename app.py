#example script
from flask import Flask, render_template, url_for, request, redirect
import requests
import os
from dotenv import load_dotenv

titles = []
app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html', titoli=titles)

if __name__ == "__main__":
    load_dotenv()  # reads .env file
    API_KEY = os.getenv("NEWS_API_KEY")
    BASE_URL = "https://newsapi.org/v2"
    HEADERS = {"X-Api-Key": API_KEY}

    params = {
        "q": "intelligenza artificiale",  # keyword(s)
        "language": "it",                 # Italian
        "from": "2025-10-01",
        "to": "2025-10-21",
        "sortBy": "publishedAt",          # relevancy | popularity | publishedAt
        "pageSize": 50,                   # up to 100
        "page": 1
    }

    response = requests.get(f"{BASE_URL}/everything", headers=HEADERS, params=params)
    data = response.json()

    for article in data.get("articles", []):
        titles.append(article["title"])

    app.run(debug=True)