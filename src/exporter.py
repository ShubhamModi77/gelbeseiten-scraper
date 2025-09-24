import pandas as pd
from typing import List, Dict
import re


def parse_address(address: str):
    """Split full address into street, postal_code, city."""
    street, postal_code, city = None, None, None
    if address:
        # Example: "Reichenbachstr. 17, 80469 München (Isarvorstadt)"
        match = re.match(r"^(.*?),\s*(\d{5})\s*(\S.*?)(?:\s*\(.*\))?$", address)
        if match:
            street, postal_code, city = match.groups()
        else:
            street = address  # fallback
    return street, postal_code, city


def items_to_df(items: List[Dict]) -> pd.DataFrame:
    rows = []
    for item in items:
        street, postal_code, city = parse_address(item.get("address"))
        rows.append(
            {
                "name": item.get("name"),
                "street": street,
                "postal_code": postal_code,
                "city": city,
                "telephone": item.get("phone"),
                "website": item.get("website"),
                "profession": item.get("profession"),
            }
        )
    df = pd.DataFrame(rows)
    return df[
        [
            "name",
            "profession" ,
            "street",
            "postal_code",
            "city",
            "telephone",
            "website",
        ]
    ]


def export_csv(df: pd.DataFrame, out_path: str) -> None:
    df.to_csv(out_path, index=False, encoding="utf-8")


def export_json(items: List[Dict], out_path: str) -> None:
    pd.DataFrame(items).to_json(out_path, orient="records", indent=2, force_ascii=False)
