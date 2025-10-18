import logging
import re
from typing import Optional

import requests
from django.db import transaction

from climate.models import (
    ClimateMonthly,
    ClimateParameter,
    ClimateRecord,
    ClimateRegion,
    ClimateSeasonal,
)
from climate.parsers.datasets import MONTH_FIELDS, SEASON_FIELDS

logger = logging.getLogger(__name__)


class ClimateDataFetcher:
    """Fetches climate data from a URL."""

    @staticmethod
    def fetch_data(url: str) -> str:
        """Fetch data from the provided URL."""

        logger.info("Fetching data from URL: %s", url)

        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            logger.info("Data fetched successfully from %s", url)
            return response.text
        except requests.exceptions.RequestException as e:
            logger.error("Error fetching data from %s: %s", url, e)
            raise


class ClimateDataParser:
    """Parses raw climate data into structured form."""

    @staticmethod
    def filter_data_lines(raw_data: str) -> list[str]:
        """Filter and prepare valid data lines from raw data."""

        lines = raw_data.splitlines()
        return [line.strip() for line in lines if re.match(r"^\d{4}", line.strip())]

    @staticmethod
    def extract_year(parts: list) -> int | None:
        """Extract the year from the parts of the line."""

        try:
            year = int(parts[0])
            return year
        except ValueError:
            logger.warning("Invalid year in line '%s'. Skipping this line.", parts)
            return None

    @staticmethod
    def extract_values(parts: list) -> list[float | None]:
        """Extract and convert values from the parts of the line."""

        # Replace "---" with None and convert the rest to float
        return [None if v == "---" else float(v) for v in parts[1:]]

    @staticmethod
    def process_months(values: list) -> dict:
        """Process the first 12 values as monthly data."""

        return dict(zip(MONTH_FIELDS, values[:12]))

    @staticmethod
    def process_seasons(values: list) -> dict:
        """Process the next 4 values as seasonal data."""

        return dict(zip(SEASON_FIELDS, values[12:]))

    @staticmethod
    def process_line(line: str) -> tuple[int, dict, dict] | None:
        """Process each line of data and return the structured data."""

        try:
            parts = line.split()
            year = ClimateDataParser.extract_year(parts)
            values = ClimateDataParser.extract_values(parts)
            month_values = ClimateDataParser.process_months(values)
            season_values = ClimateDataParser.process_seasons(values)
            return (year, month_values, season_values)

        except Exception as e:
            logger.warning("Error processing line '%s': %s", line, e)
            return None  # Skip this line

    @staticmethod
    def parse_data(raw_data: str) -> list[tuple[int, dict, dict]]:
        """Parse the raw data into structured year, month, and season data."""

        logger.info("Parsing climate data raw text.")
        data_lines = ClimateDataParser.filter_data_lines(raw_data)

        parsed_data = []
        for line in data_lines:
            parsed_line = ClimateDataParser.process_line(line)
            if parsed_line:
                parsed_data.append(parsed_line)

        return parsed_data


class ClimateDataProcessor:
    """Processes the fetched and parsed climate data and updates the database."""

    def __init__(self, region: str, dataset: str) -> None:
        logger.debug("Initializing ClimateDataProcessor for %s - %s", region, dataset)
        self.region = region
        self.dataset = dataset
        self.region_obj: Optional[ClimateRegion] = None
        self.parameter_obj: Optional[ClimateParameter] = None

    def ensure_region_and_parameter_exist(self) -> None:
        """Ensure region and parameter objects exist in the database."""

        logger.info(
            "Ensuring region and parameter exist for %s - %s", self.region, self.dataset
        )
        self.region_obj, _ = ClimateRegion.objects.get_or_create(region=self.region)
        self.parameter_obj, _ = ClimateParameter.objects.get_or_create(
            parameter=self.dataset
        )

    def fetch_or_create_record(self, year: int) -> ClimateRecord:
        """Fetch or create the ClimateRecord for the given year."""

        logger.info("Fetching or creating record for year %d", year)
        return ClimateRecord.objects.get_or_create(
            region=self.region_obj,
            parameter=self.parameter_obj,
            year=year,
        )[0]

    def upsert_monthly_data(self, record: ClimateRecord, month_values: dict) -> None:
        """Upsert the monthly data for the given record."""

        logger.info("Upserting monthly data for record %s", record)
        for idx, (month, val) in enumerate(month_values.items(), start=1):
            logger.debug(
                "Upserting monthly data for year %d, month %d", record.year, idx
            )
            ClimateMonthly.objects.update_or_create(
                record=record,
                month=idx,
                defaults={"data": val},
            )

    def upsert_seasonal_data(self, record: ClimateRecord, season_values: dict) -> None:
        """Upsert the seasonal data for the given record."""

        logger.info("Upserting seasonal data for record %s", record)
        for season, val in season_values.items():
            logger.debug(
                "Upserting seasonal data for year %d, season %s", record.year, season
            )
            ClimateSeasonal.objects.update_or_create(
                record=record,
                season=season,
                defaults={"data": val},
            )

    def update_database(
        self,
        year: int,
        month_values: dict,
        season_values: dict,
    ) -> None:
        """Update the database with the processed values."""

        logger.info("Updating database for year %d", year)
        with transaction.atomic():
            record = self.fetch_or_create_record(year)
            self.upsert_monthly_data(record, month_values)
            self.upsert_seasonal_data(record, season_values)

    def process(self, parsed_data: list[tuple[int, dict, dict]]) -> None:
        """Process a list of parsed climate data and update the database."""
        self.ensure_region_and_parameter_exist()

        for year, month_values, season_values in parsed_data:
            self.update_database(year, month_values, season_values)


class ClimateDataHandler:
    """Handles the entire process of fetching, parsing, and processing climate data."""

    def __init__(self, url: str, region: str, dataset: str) -> None:
        logger.debug("Initializing ClimateDataHandler for %s - %s", region, dataset)
        self.url = url
        self.region = region
        self.dataset = dataset

    def fetch_parse_process(self) -> None:
        """Main method to fetch, parse, and process climate data."""

        try:
            raw_data = self.fetch()
            parsed_data = self.parse(raw_data)
            self.process(parsed_data)
        except Exception as e:
            logger.error("Error during data fetching, parsing, or processing: %s", e)

    def fetch(self) -> str:
        """Fetch the raw data from the URL."""

        return ClimateDataFetcher.fetch_data(self.url)

    def parse(self, raw_data: str) -> list[tuple[int, dict, dict]]:
        """Parse the raw text data into structured format."""

        return ClimateDataParser.parse_data(raw_data)

    def process(self, parsed_data: list[tuple[int, dict, dict]]):
        """Process parsed data and update the database."""

        processor = ClimateDataProcessor(self.region, self.dataset)
        processor.ensure_region_and_parameter_exist()

        for year, month_values, season_values in parsed_data:
            processor.update_database(year, month_values, season_values)
