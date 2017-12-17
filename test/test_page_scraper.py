from os import path

from lxml.html import fromstring
from mock import Mock, patch

from webscraper.lib.page_scraper import (
    _find_links, _find_occurrences_of_words, recursively_find_words,
)

_GET_PAGE_CONTENT = 'webscraper.lib.page_scraper._get_page_content'


@patch(_GET_PAGE_CONTENT, Mock(side_effect=[fromstring('foo bar baz')]))
def test_recursively_find_words_on_one_page():
    result = recursively_find_words('url', ['foo'])
    assert {'foo': 1} == result


@patch(_GET_PAGE_CONTENT, Mock(side_effect=[
    fromstring('<a href="url2">foo1</a>'),
    fromstring('foo2')
]))
def test_recursively_find_words_on_2nd_page():
    result = recursively_find_words('url', ['foo'])
    assert {'foo': 2} == result


@patch(_GET_PAGE_CONTENT, Mock(side_effect=[
    fromstring('<a href="url2">foo1</a>'),
    fromstring('foo2')
]))
def test_recursively_respects_recurse_limit():
    result = recursively_find_words('url', ['foo'], limit=0)
    assert {'foo': 1} == result


@patch(_GET_PAGE_CONTENT, Mock(side_effect=[
    fromstring('<a href="url2">foo1</a>'),
    fromstring('<a href="url3">foo2</a>'),
    fromstring('foo3')
]))
def test_recursively_visits_no_subpages_at_limit_0():
    result = recursively_find_words('url', ['foo'], limit=0)
    assert {'foo': 1} == result


@patch(_GET_PAGE_CONTENT, Mock(side_effect=[
    fromstring('<a href="url2">foo1</a>'),
    fromstring('<a href="url3">foo2</a>'),
    fromstring('<a href="url4">foo3</a>'),
    fromstring('foo4')
]))
def test_recursively_visits_one_subpage_at_limit_2():
    result = recursively_find_words('url', ['foo'], limit=1)
    assert {'foo': 2} == result


@patch(_GET_PAGE_CONTENT, Mock(side_effect=[
    fromstring('<a href="url">foo1</a>'),
    fromstring('foo2')
]))
def test_recursively_only_visits_page_once():
    result = recursively_find_words('url', ['foo'])
    assert {'foo': 1} == result


def test_find_occurrences_of_words_in_simple_text():
    result = _find_occurrences_of_words(fromstring('foo bar bar'),
                                        ['foo', 'bar'])
    assert [('foo', 1), ('bar', 2)] == list(result)


def test_find_occurrences_of_words_against_google():
    result = _find_occurrences_of_words(_get_fixture('google.com'), ['Lucky'])
    assert [('Lucky', 1)] == list(result)


def test_find_occurrences_of_words_against_example():
    result = _find_occurrences_of_words(_get_fixture('iana.org'), ['foo'])
    assert [('foo', 0)] == list(result)


def test_find_occurrences_of_words_against_example2():
    fixture = _get_fixture('stats.research.icann.org/dns/tld_report/index.html')
    result = _find_occurrences_of_words(fixture, ['foo'])
    assert [('foo', 5)] == list(result)


def test_find_links():
    result = _find_links('/', fromstring('<a href="url">link text</a>'))
    assert 1 == len(list(result))


def test_find_links_against_google():
    result = _find_links('google.com', _get_fixture('google.com'))
    assert 24 == len(list(result))


def _get_fixture(name):
    fixture_path = path.abspath(
        path.join(path.dirname(__file__), 'fixtures', name))
    with open(fixture_path, mode='rb') as f:
        content = f.read()
        return fromstring(content)
