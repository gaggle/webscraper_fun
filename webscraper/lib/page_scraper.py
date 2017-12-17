from typing import Iterable, Iterator

import lxml.html
from requests import get
from requests.exceptions import InvalidSchema, MissingSchema


def recursively_find_words(url, words, limit=3):
    print("Visiting", url, "limit:", limit)
    word_occurrences = {}
    content = _get_page_content(url)
    if not content:
        return word_occurrences

    for word, count in _find_occurrences_of_words(content, words):
        if word not in word_occurrences:
            word_occurrences[word] = 0
        word_occurrences[word] += count

    if limit > 0:
        for sub_url in _find_links(content):
            word_occurrences.update(
                recursively_find_words(sub_url, words, limit - 1))
    return word_occurrences


def _get_page_content(url):
    try:
        res = get(url)
        content = res.text
    except (InvalidSchema, MissingSchema):
        content = ''
    return content


def _find_occurrences_of_words(content: str, words: Iterable) -> Iterator:
    occurrences = [content.count(word) for word in words]
    return zip(words, occurrences)


def _find_links(content: str) -> Iterator:
    dom = lxml.html.fromstring(content)
    for link in dom.xpath('//a/@href'):
        yield link
