from webscraper.lib.page_scraper import _get_page_content


def test_get_page_content():
    assert 'google' in _get_page_content('https://google.com').text_content()
