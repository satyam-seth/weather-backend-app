import re

import requests

from climate.models import ClimateRecord

FIELDS = [
    "jan",
    "feb",
    "mar",
    "apr",
    "may",
    "jun",
    "jul",
    "aug",
    "sep",
    "oct",
    "nov",
    "dec",
    "win",
    "spr",
    "sum",
    "aut",
    "ann",
]


def fetch_and_process_climate_data(url: str, dataset: str) -> None:
    """Parse data from the Met Office and update/create ClimateRecord entries."""

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from {url}: {e}")
        return

    # Split the response text into lines and keep those starting with a year
    lines = response.text.splitlines()
    data_lines = [line.strip() for line in lines if re.match(r"^\d{4}", line.strip())]

    for line in data_lines:
        try:
            # Split the line and extract the year and monthly/seasonal values
            parts = line.split()
            year = int(parts[0])
            values = [
                None if v == "---" else float(v) if v != "---" else None
                for v in parts[1:]
            ]

            # Create or update the record in the database
            ClimateRecord.objects.update_or_create(
                dataset=dataset,
                year=year,
                defaults=dict(zip(FIELDS, values)),
            )
        except ValueError as e:
            print(f"Error processing line '{line}': {e}")
            continue
