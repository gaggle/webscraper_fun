from flask import Flask, request, jsonify
from werkzeug.exceptions import BadRequest

from webscraper.lib.page_scraper import recursively_find_words

app = Flask(__name__)


@app.route('/ExtractInfoFromWebsite')
def extract_info_from_website():
    url = request.args.get('URL')
    raw_words = request.args.get('match_words')
    limit = int(request.args.get('recursion_depth', 3))

    if not raw_words:
        raise BadRequest("No words specified")
    words = [e.strip() for e in raw_words.split(',')]

    print("Endpoint params:", url, words, limit)
    data = recursively_find_words(url, words, limit)
    return jsonify(data)
