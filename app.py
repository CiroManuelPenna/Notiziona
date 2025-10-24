#example script
from flask import Flask, render_template, url_for, request, redirect
import requests
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta

load_dotenv()  # reads .env file
API_KEY = os.getenv("NEWS_API_KEY")
BASE_URL = "https://newsapi.org/v2"
HEADERS = {"X-Api-Key": API_KEY}
today = datetime.today()
titles = []
app = Flask(__name__)

def get_articles(params):
    response = requests.get(f"{BASE_URL}/everything", headers=HEADERS, params=params)
    data = response.json()

    if data.get("status", []) == "ok":
        return data.get("articles", [])
    else:
        print("Could not satisfy the request")
        return []
    
@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        search_terms = request.form['search_terms']
        params = {
            "q": search_terms,  # keyword(s)
            "language": "it",
            "from": (today - timedelta(days=7)).isoformat(),
            "to": today.isoformat(),
            "sortBy": "publishedAt",          # relevancy | popularity | publishedAt
            "pageSize": 50,                   # up to 100
            "page": 1
        }

        articles = get_articles(params=params)

        return render_template('index.html', articles=articles)
    else:
        return render_template('index.html', articles=[])

if __name__ == "__main__":
    app.run(debug=True)