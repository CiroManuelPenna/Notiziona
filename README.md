# About the project
Notiziona is a news feed, based on newsapi.org
The app consists of four sections:
- home: shows top headlines
- search: lets the user search news based on keywords and/or categories
- favorites: shows the user's favorite articles
- feed: shows a feed based on user's favorite keywords and categories

# How to Run the Project

### 1. Get an API Key
- Create an account at [newsapi.org](https://newsapi.org)
- Copy your free API key

### 2. Set Up Environment Variables
Create a file named `.env` in the project root and add your key:

```NEWS_API_KEY=your_api_key_here```

### 3. Create and Activate a Virtual Environment
Make sure you have a working python installation. Run the following commands:

```
pip install virtualenv
virtualenv venv
source venv/bin/activate
```

### 4. Install the dependencies
```
pip install -r requirements.txt
```

### 5. Run the application
```
python3 app.py
```