from os import path

from webscraber.lib.page_scraper import (
    _find_occurrences_of_words, _get_page_content,
)


def test_get_page_content():
    assert '<head>' in _get_page_content('https://google.com')


def test_find_occurrences_of_words_in_simple_text():
    result = _find_occurrences_of_words('foo bar bar', ['foo', 'bar'])
    assert list(result) == [('foo', 1), ('bar', 2)]


def test_find_occurrences_of_words_against_google():
    result = _find_occurrences_of_words(_get_fixture('google.com'), ['Lucky'])
    assert list(result) == [('Lucky', 2)]


def _get_fixture(name):
    fixture_path = path.abspath(path.join('fixtures', name))
    with open(fixture_path) as f:
        return f.read()
