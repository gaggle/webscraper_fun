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

To start:
```
export FLASK_APP=webscraper/app.py
flask run
```

Use it:

Make request to `http://127.0.0.1:5000/ExtractInfoFromWebsite?url=http://example.com&words=example,foo&limit=0`
```
