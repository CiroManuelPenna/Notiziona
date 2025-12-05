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
CATEGORIES = [
    "business",
    "entertainment",
    "general",
    "health",
    "science",
    "sports",
    "technology"
]
today = datetime.today()

class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    url = db.Column(db.String(200), nullable=False)
    image_url = db.Column(db.String(200))

    def __repr__(self):
        return '<Article %r>' % self.id
    
class FavoriteTerm(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    term = db.Column(db.String(200), unique=True, nullable=False)
    type = db.Column(db.String(50), nullable=False)   # "keyword" or "category"

with app.app_context():
    db.create_all()


def is_favorited(url):
    return Article.query.filter_by(url=url).first() is not None

app.jinja_env.globals.update(is_favorited=is_favorited)

def is_favorite_term(term, type_):
    return FavoriteTerm.query.filter_by(term=term, type=type_).first() is not None

app.jinja_env.globals.update(is_favorite_term=is_favorite_term)


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
    if request.method == "POST":
        keyword = request.form.get("search_terms")
        category = request.form.get("category")

        if category and keyword:
            params = {
                "q": keyword,
                "category": category,
                "country": "us",
                "pageSize": 50
            }
            articles = get_top_headlines(params)
        elif category:
            params = {
                "category": category,
                "country": "us",
                "pageSize": 50
            }
            articles = get_top_headlines(params)
        else:
            params = {
                "q": keyword,
                "language": "en",
                "from": (today - timedelta(days=7)).isoformat(),
                "to": today.isoformat(),
                "sortBy": "publishedAt",
                "pageSize": 50
            }
            articles = get_articles(params)

        return render_template(
            "search_page.html",
            articles=articles,
            categories=CATEGORIES,
            keyword=keyword,
            selected_category=category
        )

    return render_template("search_page.html", articles=[], categories=CATEGORIES)

    
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

@app.route("/api/favterm/add", methods=["POST"])
def api_term_add():
    data = request.get_json()
    term = data["term"]
    type_ = data["type"]

    existing = FavoriteTerm.query.filter_by(term=term).first()
    if existing:
        return {"status": "exists"}

    new = FavoriteTerm(term=term, type=type_)
    db.session.add(new)
    db.session.commit()
    return {"status": "added"}

@app.route("/api/favterm/remove", methods=["POST"])
def api_term_remove():
    data = request.get_json()
    term = data["term"]

    existing = FavoriteTerm.query.filter_by(term=term).first()
    if not existing:
        return {"status": "not_found"}, 404

    db.session.delete(existing)
    db.session.commit()
    return {"status": "removed"}


if __name__ == "__main__":
    app.run(debug=True)