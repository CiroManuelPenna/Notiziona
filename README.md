# How to run
- Create an account on newsapi.org to get a free API key
- Create a .env file and write in it: NEWS_API_KEY=your_api_key
- run:
pip install virtualenv
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
python3 app.py
- visit the webpage (it should open on port 5000 by default)