from flask import Flask, request, jsonify
from werkzeug.exceptions import BadRequest

from webscraper.lib.page_scraper import recursively_find_words

app = Flask(__name__)


@app.route('/ExtractInfoFromWebsite')
def extract_info_from_website():
    url = request.args.get('url')
    raw_words = request.args.get('words')
    if not raw_words:
        raise BadRequest("No words specified")
    words = [e.strip() for e in raw_words.split(',')]
    limit = int(request.args.get('limit', 3))
    print("Endpoint params:", url, words, limit)
    data = recursively_find_words(url, words, limit)
    return jsonify(data)
