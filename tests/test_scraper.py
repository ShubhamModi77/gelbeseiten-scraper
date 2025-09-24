import pytest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from src.scraper import GelbeSeitenScraper

# Dummy HTML to simulate a listing
sample_html = """
<html>
<body>
<article class="mod-Treffer">
    <h2 class="mod-Treffer__name">Dr. Olsen Schewtschenko Kanzlei für Arbeitsrecht</h2>
    <div class="mod-AdresseKompakt__adress-text">Sonnenstr. 32, 80331 München (Ludwigsvorstadt)</div>
    <a class="mod-TelefonnummerKompakt__phoneNumber">089 21 54 89 40</a>
    <div class="mod-WebseiteKompakt"><a href="https://example-website.de">Webseite</a></div>
    <span class="mod-BewertungKompakt__number">4,9</span>
    <span class="mod-BewertungKompakt__text">212 Bewertungen</span>
    <p class="mod-Treffer--besteBranche">Rechtsanwälte</p>
</article>
</body>
</html>
"""


class DummyDriver:
    def get(self, url):
        pass

    @property
    def page_source(self):
        return sample_html

    def find_element(self, by, value):
        # Simulate "no next page"
        from selenium.common.exceptions import NoSuchElementException

        raise NoSuchElementException()

    def quit(self):
        pass


def test_fetch_listings_basic():
    scraper = GelbeSeitenScraper(location="München", max_pages=1)
    scraper.driver = DummyDriver()
    results = scraper.fetch_listings("rechtsanwalt")

    # Only one article should be parsed
    assert len(results) == 1
    item = results[0]

    assert item["name"] == "Dr. Olsen Schewtschenko Kanzlei für Arbeitsrecht"
    assert item["address"] == "Sonnenstr. 32, 80331 München (Ludwigsvorstadt)"
    assert item["phone"] == "089 21 54 89 40"
    assert item["website"] == "https://example-website.de"
    assert item["rating"] == "4,9"
    assert item["reviews"] == "212 Bewertungen"
    assert item["category"] == "Rechtsanwälte"
    assert item["location"] == "München"


def test_fetch_listings_empty():
    class EmptyDriver(DummyDriver):
        @property
        def page_source(self):
            return "<html><body></body></html>"

    scraper = GelbeSeitenScraper(location="Berlin", max_pages=1)
    scraper.driver = EmptyDriver()
    results = scraper.fetch_listings("arzt")
    assert results == []
