import argparse
import os
import re
import logging
import time
import json
from scraper import GelbeSeitenScraper
from exporter import items_to_df, export_csv, export_json


def scrape_profession(scraper, profession):
    return scraper.fetch_listings(profession)


def scrape_and_save(professions, location, output_dir="results", debug=False):
    results_dir = os.path.abspath(output_dir)
    os.makedirs(results_dir, exist_ok=True)

    scraper = GelbeSeitenScraper(location=location, debug=debug)
    all_results = []

    start_time = time.time()

    # metrics container
    metrics = {"location": location, "professions": {}, "totals": {}}

    for idx, prof in enumerate(professions, 1):
        print(f"\n--- [{idx}/{len(professions)}] Scraping profession: {prof} ---")
        prof_start = time.time()

        try:
            results = scrape_profession(scraper, prof)
            total = len(results)

            if not results:
                print(f"No results found for {prof}")
                continue

            safe_prof = re.sub(r"\W+", "_", prof.lower())
            safe_location = re.sub(r"\W+", "_", location.lower()) if location else "all"

            # Save CSV
            df = items_to_df(results)
            csv_file = os.path.join(results_dir, f"{safe_prof}_{safe_location}.csv")
            export_csv(df, csv_file)
            print(f"{prof}: {total} entries saved to {csv_file}")

            # Save JSON
            json_file = os.path.join(results_dir, f"{safe_prof}_{safe_location}.json")
            export_json(results, json_file)
            print(f" {prof}: JSON saved to {json_file}")

            all_results.extend(results)
            print(f"Total scraped so far: {len(all_results)} entries")

        except Exception as e:
            logging.exception(f"Failed to scrape {prof}: {e}")
            total = 0  # ensure metric still exists

        # Timing for this profession
        prof_elapsed = time.time() - prof_start
        avg_time = (time.time() - start_time) / idx
        remaining = avg_time * (len(professions) - idx)

        print(
            f"{prof} took {prof_elapsed:.1f}s | "
            f"Elapsed: {(time.time() - start_time):.1f}s | "
            f"ETA: ~{remaining:.1f}s"
        )

        # save metrics for this profession
        metrics["professions"][prof] = {
            "entries": total,
            "time_sec": round(prof_elapsed, 1),
        }

    # totals
    total_time = time.time() - start_time
    print(f"Finished scraping in {total_time:.1f} seconds.")
    metrics["totals"] = {
        "entries": len(all_results),
        "time_sec": round(total_time, 1),
        "time_min": round(total_time / 60, 1),
    }

    # write metrics file
    metrics_file = os.path.join(results_dir, f"metrics_{safe_location}.json")
    with open(metrics_file, "w", encoding="utf-8") as f:
        json.dump(metrics, f, ensure_ascii=False, indent=2)
    print(f"Metrics saved to {metrics_file}")

    scraper.close()


def main():
    parser = argparse.ArgumentParser(description="GelbeSeiten scraper")
    parser.add_argument("--input-file", help="Text file with one profession per line")
    parser.add_argument("--location", required=True, help="City or region")
    parser.add_argument("--debug", action="store_true", help="Print HTML debug output")
    args = parser.parse_args()

    default_professions = [
        "sanitärinstallation",
        "elektroinstallationen",
        "steuerberatung",
        "arzt",
        "rechtsanwalt",
    ]

    if args.input_file:
        input_path = os.path.abspath(args.input_file)
        if not os.path.exists(input_path):
            raise FileNotFoundError(f"Input file not found: {input_path}")
        with open(input_path, "r", encoding="utf-8") as f:
            professions = [line.strip().lower() for line in f if line.strip()]
    else:
        professions = default_professions

    print(f"Professions to scrape: {professions}")
    print(f"Location: {args.location}")

    scrape_and_save(professions, location=args.location, debug=args.debug)


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
    )
    main()
