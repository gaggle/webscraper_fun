from typing import Iterable, Iterator

import requests


def recursively_find_words(url, words, limit=3):
    word_occurrences = {}
    content = _get_page_content(url)

    word_occurrences.update(_find_occurrences_of_words(content, words))
    for link in _yield_links():
        recursively_find_words(link, words, limit - 1)
    return {}


def _get_page_content(url):
    res = requests.get(url)
    content = res.text
    return content


def _find_occurrences_of_words(content: str, words: Iterable) -> Iterator:
    occurrences = [content.count(word) for word in words]
    return zip(words, occurrences)


def _yield_links():
    yield ''
