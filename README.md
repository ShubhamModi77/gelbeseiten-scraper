# GelbeSeiten Scraper

A Python scraper for [GelbeSeiten.de](https://www.gelbeseiten.de), the German Yellow Pages.
It extracts business listings by **profession** and **location**, then exports the data to **CSV**, **JSON** and a **metrics summary**

---

## Features

- Scrapes listings for any profession and location.
- Extracts:
  - Company/Person name
  - Address (split into street, postal code, city)
  - Telephone number
  - Website
  - Profession & category
  - Ratings and reviews (if available)
- Handles pagination (`Mehr Anzeigen` button).
- Saves data as:
  - **CSV**
  - **JSON**
  - **Metrics JSON**
- Configurable via CLI arguments.
- Includes unit tests with `pytest`.

---

## Requirements

- **Python:** 3.12.4
- **pip:** 23+
- **Libraries:** `selenium`, `webdriver-manager`, `beautifulsoup4`, `pandas`
- **Google Chrome & ChromeDriver**

## Installation (Local)

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/gelbeseiten-scraper.git
   cd gelbeseiten-scraper
   ```

2. Create and activate a virtual environment:
    ```
    python -m venv venv
    # Windows
    venv\Scripts\activate
    # Linux/macOS
    source venv/bin/activate
    ```

3. Install dependencies:
    ```
    pip install -r requirements.txt
    ```

## Usage

Basic command:
```
python src/main.py --location "München"
```

This will scrape the default professions (sanitärinstallation, elektroinstallationen, steuerberatung, arzt, rechtsanwalt) for München.

With custom input file:
```
python src/main.py --location "München" --input-file professions.txt
```

## Output
All results are stored in the `results/` directory:

- Per profession:

  - arzt_muenchen.csv

  -  arzt_muenchen.json
  -  sanitärinstallation.json
  -  sanitärinstallation.csv
  -  Elektroinstallationen.json
  -  Elektroinstallationen.csv
  -  Steuerberatung.json
  -  Steuerberatung.csv
  -  Rechtsanwälte.json
  -  Rechtsanwälte.csv

- Metrics:

    - metrics_münchen.json

## Testing
```
pytest -v
```
Tests use a dummy HTML driver so no live requests are made.

