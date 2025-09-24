# GelbeSeiten Scraper

---

## 1. Overview

The scraper automates the extraction of business listings from **GelbeSeiten.de**.
It uses **Selenium** to load and paginate listings and **BeautifulSoup** for parsing HTML content.
Extracted data is transformed into structured formats (CSV/JSON) and summarized in a **metrics file** for evaluation.

---

## 2. Architecture

### 2.1 Module Structure

- **`scraper.py`**
  - `GelbeSeitenScraper` class
  - Manages Selenium WebDriver lifecycle
  - Handles page loading, HTML parsing, pagination, and data extraction

- **`main.py`**
  - Command-line entry point
  - Reads CLI arguments (professions, location)
  - Orchestrates scraping for multiple professions
  - Collects runtime metrics and saves them as JSON

- **`exporter.py`**
  - Data transformation and export utilities
  - Parses addresses into `street`, `postal_code`, and `city`
  - Exports data to **CSV** (normalized format) and **JSON** (raw format)

- **`test_scraper.py`**
  - Unit tests with `pytest`
  - Uses **DummyDriver** and **sample HTML** to simulate Selenium output
  - Tests parsing logic and empty results handling

### 2.2 Component Interaction

![Architecture Diagram](images/image.png)

---

## 3. Data Flow Diagram (DFD)

### 3.1 Level 1 (High-Level)

![Data Flow Diagram](images/image_1.png)

### 3.2 Level 2 (Scraping Workflow)

![Scraping Workflow](images/image_2.png)

---

## 4. Data Model

### 4.1 Listing Data (JSON)

Each listing is represented as a dictionary:

```json
{
  "name": "Dr. Olsen Schewtschenko Kanzlei für Arbeitsrecht",
  "profession": "rechtsanwalt",
  "location": "München",
  "address": "Sonnenstr. 32, 80331 München (Ludwigsvorstadt)",
  "phone": "089 21 54 89 40",
  "rating": "4,9",
  "reviews": "212 Bewertungen",
  "category": "Rechtsanwälte",
  "website": "https://example-website.de"
}

```
### 4.2 Listing Data (CSV)

In addition to JSON, listings are exported in CSV format with normalized fields.

```CSV
name,profession,street,postal_code,city,telephone,website
Dr. Olsen Schewtschenko Kanzlei für Arbeitsrecht,rechtsanwalt,Sonnenstr. 32,80331,München,089 21 54 89 40,https://example-website.de
```

### 4.3 Metrics Data

The scraper also generates a metrics_<location>.json file summarizing the run:
```Json
{
  "location": "München",
  "professions": {
    "sanitärinstallation": {"entries": 4293, "time_sec": 203.6},
    "elektroinstallationen": {"entries": 4593, "time_sec": 216.5},
    "steuerberatung": {"entries": 44590, "time_sec": 775.6},
    "arzt": {"entries": 3720, "time_sec": 196.5},
    "rechtsanwalt": {"entries": 268263, "time_sec": 2486.4}
  },
  "totals": {
    "entries": 325459,
    "time_sec": 3878.6,
    "time_min": 64.6
  }
}
```
