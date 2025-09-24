import json
import os
import time
from typing import List, Dict

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup


class GelbeSeitenScraper:
    def __init__(self, location: str, debug: bool = False):
        self.base_url = "https://www.gelbeseiten.de/branchen/"
        self.location = location
        self.debug = debug

        # Selenium setup
        chrome_options = Options()
        chrome_options.add_argument("--headless=new")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--window-size=1920,1080")
        self.driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()), options=chrome_options
        )

    def _safe_int(self, element_id: str) -> int:
        """Return int value of element text or 0 if not found/empty."""
        try:
            elem = self.driver.find_element(By.ID, element_id)
            txt = elem.text.strip().replace(".", "")  # remove thousand separators
            return int(txt) if txt else 0
        except Exception:
            return 0

    def fetch_listings(self, profession: str) -> List[Dict]:
        url = f"{self.base_url}{profession}/{self.location}"
        listings = []

        self.driver.get(url)
        time.sleep(3)
        while True:
            if self.debug:
                print(f"[Scraper] Extracting data...")

            html = self.driver.page_source
            soup = BeautifulSoup(html, "html.parser")
            page_listings = []

            for item in soup.select("article.mod-Treffer"):
                name = item.select_one("h2.mod-Treffer__name")
                address = item.select_one(".mod-AdresseKompakt__adress-text")
                phone = item.select_one(".mod-TelefonnummerKompakt__phoneNumber")
                rating = item.select_one(".mod-BewertungKompakt__number")
                reviews = item.select_one(".mod-BewertungKompakt__text")
                category = item.select_one("p.mod-Treffer--besteBranche")
                website = item.select_one(".mod-WebseiteKompakt a")

                if name:
                    page_listings.append(
                        {
                            "name": name.get_text(strip=True),
                            "profession": profession,
                            "location": self.location,
                            "address": (address.get_text(" ", strip=True) if address else None),
                            "phone": phone.get_text(strip=True) if phone else None,
                            "rating": rating.get_text(strip=True) if rating else None,
                            "reviews": (reviews.get_text(strip=True) if reviews else None),
                            "category": (category.get_text(strip=True) if category else None),
                            "website": (website["href"]if website and website.has_attr("href") else None),
                        }
                    )

            if not page_listings:
                if self.debug:
                    print("[Scraper] No listings found on this page. Stopping.")
                break

            listings.extend(page_listings)

            # Progress tracking
            try:
                shown = self.driver.find_element(By.ID, "loadMoreGezeigteAnzahl").text
                total = self.driver.find_element(By.ID, "loadMoreGesamtzahl").text
                if self.debug:
                    print(f"[Scraper] Progress: {shown}/{total} entries loaded")
            except NoSuchElementException:
                # If the progress indicators aren't found, it's likely the end.
                pass

            # Try to find and click "Mehr Anzeigen"
            try:
                load_more = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.ID, "mod-LoadMore--button"))
                )
                ActionChains(self.driver).move_to_element(load_more).click().perform()
                time.sleep(2)  # allow new results to load
            except (TimeoutException, NoSuchElementException):
                if self.debug:
                    print(
                        "[Scraper] No 'Mehr Anzeigen' button found or it's not clickable. Ending pagination."
                    )
                break

        if self.debug:
            print(f"[Scraper] Total listings found for '{profession}': {len(listings)}")

        return listings

    def save_json(self, data: List[Dict], filename: str):
        os.makedirs("output", exist_ok=True)
        path = os.path.join("output", filename)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def close(self):
        self.driver.quit()
