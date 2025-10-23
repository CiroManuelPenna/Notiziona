#example script

import requests
import os
from dotenv import load_dotenv


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
    print(article["title"])

print("")
print("")
print("")
print("")

print(data.get("articles", [])[1]["content"])

"""
Response structure:
{
  "status": "ok",
  "totalResults": <int>,
  "articles": [ … ]
}

Each article has fields:

source: object with id, name 

author: string 

title: string 

description: string 

url: string 

urlToImage: string 

publishedAt: string datetime in UTC 

content: string (truncated to ~200 chars)
"""