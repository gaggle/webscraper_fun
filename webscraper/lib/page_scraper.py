from typing import Iterable, Iterator

import lxml.html
from requests import get


def recursively_find_words(url, words, limit=3):
    word_occurrences = {}
    content = _get_page_content(url)

    word_occurrences.update(_find_occurrences_of_words(content, words))
    for link in _find_links(content):
        recursively_find_words(link, words, limit - 1)
    return {}


def _get_page_content(url):
    res = get(url)
    content = res.text
    return content


def _find_occurrences_of_words(content: str, words: Iterable) -> Iterator:
    occurrences = [content.count(word) for word in words]
    return zip(words, occurrences)


def _find_links(content: str) -> Iterator:
    dom = lxml.html.fromstring(content)
    for link in dom.xpath('//a/@href'):
        yield link
