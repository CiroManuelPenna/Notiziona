# How to Run the Project

### 1. Get an API Key
- Create an account at [newsapi.org](https://newsapi.org)
- Copy your free API key

### 2. Set Up Environment Variables
Create a file named `.env` in the project root and add your key:

```NEWS_API_KEY=your_api_key_here```

### 3. Create and Activate a Virtual Environment
Run the following commands:

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