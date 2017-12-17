from os import path

from lxml.html import fromstring
from mock import Mock, patch

from webscraper.lib.page_scraper import (
    _find_links, _find_occurrences_of_words, recursively_find_words,
)


@patch('webscraper.lib.page_scraper._get_page_content',
       Mock(side_effect=[fromstring('foo bar baz')]))
def test_recursively_find_words_on_one_page():
    result = recursively_find_words('n/a', ['foo'])
    assert result == {'foo': 1}


@patch('webscraper.lib.page_scraper._get_page_content',
       Mock(side_effect=[fromstring('<a href="url">link text</a>'),
                         fromstring('foo')]))
def test_recursively_find_words_on_2nd_page():
    result = recursively_find_words('n/a', ['foo'])
    assert result == {'foo': 1}


@patch('webscraper.lib.page_scraper._get_page_content',
       Mock(side_effect=[fromstring('<a href="url">foo</a>'),
                         fromstring('foo')]))
def test_recursively_respects_recurse_limit():
    result = recursively_find_words('n/a', ['foo'], limit=0)
    assert result == {'foo': 1}


@patch('webscraper.lib.page_scraper._get_page_content',
       Mock(side_effect=[fromstring('<a href="url">foo</a>'),
                         fromstring('<a href="url">foo</a>'),
                         fromstring('<a href="url">foo</a>')]))
def test_recursively_visits_one_depth_at_limit_1():
    result = recursively_find_words('n/a', ['foo'], limit=1)
    assert result == {'foo': 2}


@patch('webscraper.lib.page_scraper._get_page_content',
       Mock(side_effect=[
           fromstring('<a href="url">link text</a>foo'),
           fromstring('foo')
       ]))
def test_recursively_only_visits_page_once():
    result = recursively_find_words('url', ['foo'])
    assert result == {'foo': 1}


def test_find_occurrences_of_words_in_simple_text():
    result = _find_occurrences_of_words(fromstring('foo bar bar'),
                                        ['foo', 'bar'])
    assert list(result) == [('foo', 1), ('bar', 2)]


def test_find_occurrences_of_words_against_google():
    result = _find_occurrences_of_words(_get_fixture('google.com'), ['Lucky'])
    assert list(result) == [('Lucky', 1)]


def test_find_occurrences_of_words_against_example():
    result = _find_occurrences_of_words(_get_fixture('iana.org'), ['foo'])
    assert list(result) == [('foo', 0)]


def test_find_occurrences_of_words_against_example2():
    fixture = _get_fixture('stats.research.icann.org/dns/tld_report/index.html')
    result = _find_occurrences_of_words(fixture, ['foo'])
    assert list(result) == [('foo', 5)]


def test_find_links():
    result = _find_links('/', fromstring('<a href="url">link text</a>'))
    assert len(list(result)) == 1


def test_find_links_against_google():
    result = _find_links('google.com', _get_fixture('google.com'))
    assert len(list(result)) == 24


def _get_fixture(name):
    fixture_path = path.abspath(
        path.join(path.dirname(__file__), 'fixtures', name))
    with open(fixture_path, mode='rb') as f:
        content = f.read()
        return fromstring(content)
