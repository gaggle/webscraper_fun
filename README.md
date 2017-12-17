# webscraper_fun

Install:
```
python -v venv env
source env/bin/activate
pip install -r requirements.txt -r test_requirements.txt
```

Test:
```
PYTHONPATH=. pytest test
```

To start dev:
```
export FLASK_APP=webscraper/app.py
flask run
```

To start "production":
```
cd webscraper
PYTHONPATH=. gunicorn --bind 0.0.0.0:8000 wsgi:app --workers 10

```

Use it:

Make request to `http://127.0.0.1:5000/ExtractInfoFromWebsite?URL=http://example.com&match_words=example,foo&recursion_depth=0`
```
