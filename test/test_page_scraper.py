from os import path

from mock import Mock, patch

from webscraper.lib.page_scraper import (
    _find_links, _find_occurrences_of_words, _get_page_content,
    recursively_find_words,
)


@patch('webscraper.lib.page_scraper._get_page_content',
       Mock(side_effect=['foo bar baz']))
def test_recursively_find_words_on_one_page():
    result = recursively_find_words('n/a', ['foo'])
    assert result == {'foo': 1}


@patch('webscraper.lib.page_scraper._get_page_content',
       Mock(side_effect=['<a href="url">link text</a>', 'foo']))
def test_recursively_find_words_on_2nd_page():
    result = recursively_find_words('n/a', ['foo'])
    assert result == {'foo': 1}

@patch('webscraper.lib.page_scraper._get_page_content',
       Mock(side_effect=['<a href="url">link text</a>', 'foo']))
def test_recursively_respects_recurse_limit():
    result = recursively_find_words('n/a', ['foo'], limit=0)
    assert result == {'foo': 0}


def test_get_page_content():
    assert '<head>' in _get_page_content('https://google.com')


def test_find_occurrences_of_words_in_simple_text():
    result = _find_occurrences_of_words('foo bar bar', ['foo', 'bar'])
    assert list(result) == [('foo', 1), ('bar', 2)]


def test_find_occurrences_of_words_against_google():
    result = _find_occurrences_of_words(_get_fixture('google.com'), ['Lucky'])
    assert list(result) == [('Lucky', 2)]


def test_find_links_against_google():
    result = _find_links(_get_fixture('google.com'))
    assert len(list(result)) == 20


def _get_fixture(name):
    fixture_path = path.abspath(path.join(path.dirname(__file__), 'fixtures', name))
    with open(fixture_path) as f:
        return f.read()
