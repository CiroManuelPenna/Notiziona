#example script
from flask import Flask, render_template, url_for, request, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy
import requests
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///notiziona.db'
db = SQLAlchemy(app)
load_dotenv()  # reads .env file
API_KEY = os.getenv("NEWS_API_KEY")
BASE_URL = "https://newsapi.org/v2"
HEADERS = {"X-Api-Key": API_KEY}
today = datetime.today()

class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    url = db.Column(db.String(200), nullable=False)
    image_url = db.Column(db.String(200))

    def __repr__(self):
        return '<Article %r>' % self.id
    

with app.app_context():
    db.create_all()


def is_favorited(url):
    return Article.query.filter_by(url=url).first() is not None

app.jinja_env.globals.update(is_favorited=is_favorited)


def get_articles(params):
    response = requests.get(f"{BASE_URL}/everything", headers=HEADERS, params=params)
    data = response.json()

    if data.get("status", []) == "ok":
        return data.get("articles", [])
    else:
        print("Could not satisfy the request")
        return []
    
def get_top_headlines(params=None):
    if params is None:
        # minimal valid parameter (NewsAPI requires at least one)
        params = {"country": "us"}

    response = requests.get(f"{BASE_URL}/top-headlines", headers=HEADERS, params=params)
    data = response.json()

    if data.get("status") == "ok":
        return data.get("articles", [])
    else:
        print("Could not satisfy the request")
        return []
    
@app.route("/", methods=['GET'])
def index():
    articles = get_top_headlines()
    return render_template('index.html', articles=articles)

@app.route("/search", methods=['GET', 'POST'])
def search_page():
    if request.method == 'POST':
        search_terms = request.form['search_terms']
        params = {
            "q": search_terms,  # keyword(s)
            "language": "en",
            "from": (today - timedelta(days=7)).isoformat(),
            "to": today.isoformat(),
            "sortBy": "publishedAt",          # relevancy | popularity | publishedAt
            "pageSize": 50,                   # up to 100
            "page": 1
        }

        articles = get_articles(params=params)

        return render_template('search_page.html', articles=articles)
    else:
        return render_template('search_page.html', articles=[])
    
@app.route("/favorites", methods=['GET'])
def favorites():
    articles = Article.query.all()
    return render_template("favorites.html", articles=articles)

@app.route("/api/favorite/add", methods=["POST"])
def api_favorite_add():
    data = request.json
    url = data["url"]
    title = data["title"]
    image = data.get("image")

    existing = Article.query.filter_by(url=url).first()
    if existing:
        return jsonify({"status": "exists"}), 200

    article = Article(title=title, url=url, image_url=image)
    db.session.add(article)
    db.session.commit()

    return jsonify({"status": "added"}), 200


@app.route("/api/favorite/remove", methods=["POST"])
def api_favorite_remove():
    data = request.json
    url = data["url"]

    article = Article.query.filter_by(url=url).first()
    if not article:
        return jsonify({"status": "not_found"}), 404

    db.session.delete(article)
    db.session.commit()

    return jsonify({"status": "removed"}), 200


if __name__ == "__main__":
    app.run(debug=True)