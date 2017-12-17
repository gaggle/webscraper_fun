from typing import Iterable, Iterator, Optional
from urllib.parse import urljoin

import lxml.html
from requests import get


def recursively_find_words(url, words, limit=3, visited=None):
    if visited is None:
        visited = []
    word_occurrences = {}
    print("Visiting", url, "limit:", limit)
    html = _get_page_content(url)
    visited.append(url)
    if html is None:
        return word_occurrences

    for word, count in _find_occurrences_of_words(html, words):
        if word not in word_occurrences:
            word_occurrences[word] = 0
        word_occurrences[word] += count

    if limit > 0:
        for sub_url in _find_links(url, html):
            if sub_url in visited:
                continue
            sub_page_words = recursively_find_words(sub_url, words, limit - 1)
            word_occurrences = _combine_word_occurrences(word_occurrences,
                                                         sub_page_words)
    return word_occurrences


def _combine_word_occurrences(a: dict, b: dict) -> dict:
    result = a.copy()
    for k, v in b.items():
        if k not in result:
            result[k] = v
        else:
            result[k] += v
    return result


def _get_page_content(url) -> Optional[lxml.html.HtmlElement]:
    try:
        res = get(url)
        return lxml.html.fromstring(res.text)
    except Exception as ex:
        print("Giving up getting URL '{}': {}".format(url, ex))
        return None


def _find_occurrences_of_words(dom: lxml.html.HtmlElement,
                               words: Iterable) -> Iterator:
    content = dom.text_content()
    occurrences = [content.count(word) for word in words]
    return zip(words, occurrences)


def _find_links(root: str, dom: lxml.html.HtmlElement) -> Iterator:
    for element, attribute, link, pos in dom.iterlinks():
        yield urljoin(root, link)
