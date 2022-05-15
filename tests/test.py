import unittest

from starlette.testclient import TestClient

from app import app
from services.factory import Base64Shortener, Shortener, CustomShortener


class _AbstractShortenerTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.base_url = ''
        self.real_url = ''
        self.expected_short_slug = ''
        self.expected_short_url = ''
        self.shortener = Shortener(url=self.real_url)

    def test_url_short_(self):
        url_shorted = self.shortener.shorten()
        self.assertEqual(self.expected_short_url, url_shorted)

    def test_url_slug_equal_expected_shorten_slug(self):
        short_slug = self.shortener._encode_slug()
        self.assertEqual(self.expected_short_slug, short_slug)

    def test_url_enlarge_equal_real_url(self):
        self.shortener.slug = self.expected_short_slug
        url_enlarged = self.shortener.enlarge()
        self.assertEqual(self.real_url, url_enlarged)


class ShortenerBase64TestCase(_AbstractShortenerTestCase):

    def setUp(self) -> None:
        self.base_url = 'http://127.0.0.1:8000/'
        self.real_url = 'https://www.google.com/'
        self.expected_short_slug = 'aHR0cHM6Ly93d3cuZ29vZ2xlLmNvbS8='
        self.expected_short_url = f'{self.base_url}v1/aHR0cHM6Ly93d3cuZ29vZ2xlLmNvbS8='
        self.shortener = Base64Shortener(url=self.real_url, base_url=self.base_url)


class ShortenerCustomTestCase(_AbstractShortenerTestCase):

    def setUp(self) -> None:
        with TestClient(app):
            self.base_url = 'http://127.0.0.1:8000/'
            self.real_url = 'https://www.google.com/'
            self.expected_short_slug = 1744898168
            self.expected_short_url = f'{self.base_url}v1/1744898168'
            self.shortener = CustomShortener(url=self.real_url, base_url=self.base_url)


del _AbstractShortenerTestCase

if __name__ == '__main__':
    unittest.main()
