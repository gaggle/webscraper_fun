from typing import Iterable, Iterator
from urllib.parse import urljoin

import lxml.html
from requests import get


def recursively_find_words(url, words, limit=3, visited=[]):
    word_occurrences = {}
    print("Visiting", url, "limit:", limit)
    content = _get_page_content(url)
    visited.append(url)
    if not content:
        return word_occurrences

    for word, count in _find_occurrences_of_words(content, words):
        if word not in word_occurrences:
            word_occurrences[word] = 0
        word_occurrences[word] += count

    if limit > 0:
        for sub_url in _find_links(url, content):
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


def _get_page_content(url):
    try:
        res = get(url)
        content = res.text
    except Exception as ex:
        print("Giving up getting URL '{}': {}".format(url, ex))
        content = ''
    return content


def _find_occurrences_of_words(content: str, words: Iterable) -> Iterator:
    occurrences = [content.count(word) for word in words]
    return zip(words, occurrences)


def _find_links(root:str, content: str) -> Iterator:
    dom = lxml.html.fromstring(content)
    for link in dom.xpath('//a/@href'):
        yield urljoin(root, link)
