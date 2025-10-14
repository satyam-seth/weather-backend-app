import re

import requests
from django.db import transaction

from climate.models import (
    ClimateMonthly,
    ClimateParameter,
    ClimateRecord,
    ClimateRegion,
    ClimateSeasonal,
)
from climate.parser.datasets import MONTH_FIELDS, SEASON_FIELDS


def fetch_and_process_climate_data(url: str, region: str, dataset: str) -> None:
    """Parse data from the Met Office and update/create Database entries."""

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from {url}: {e}")
        return

    lines = response.text.splitlines()
    data_lines = [line.strip() for line in lines if re.match(r"^\d{4}", line.strip())]

    # Ensure region and parameter exist
    region_obj, _ = ClimateRegion.objects.get_or_create(region=region)
    parameter_obj, _ = ClimateParameter.objects.get_or_create(parameter=dataset)

    for line in data_lines:
        try:
            parts = line.split()
            year = int(parts[0])
            values = [None if v == "---" else float(v) for v in parts[1:]]

            month_values = dict(zip(MONTH_FIELDS, values[:12]))
            season_values = dict(zip(SEASON_FIELDS, values[12:]))

            with transaction.atomic():
                record, _ = ClimateRecord.objects.get_or_create(
                    region=region_obj,
                    parameter=parameter_obj,
                    year=year,
                )

                # Upsert monthly data
                for idx, (month, val) in enumerate(month_values.items(), start=1):
                    ClimateMonthly.objects.update_or_create(
                        record=record,
                        month=idx,
                        defaults={"data": val},
                    )

                # Upsert seasonal data
                for season, val in season_values.items():
                    ClimateSeasonal.objects.update_or_create(
                        record=record,
                        season=season,  # "win", "spr", ...
                        defaults={"data": val},
                    )

        except Exception as e:
            print(f"Error processing line '{line}': {e}")
            continue
