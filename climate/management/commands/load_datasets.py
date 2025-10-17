from django.core.management.base import BaseCommand

from climate.parsers import DATASETS, REGIONS, ClimateDataHandler


class Command(BaseCommand):
    """Management command to load climate datasets"""

    help = "Load Met Office climate datasets"

    def handle(self, *args, **kwargs):
        """Handle command to fetch and parse datasets."""

        for region in REGIONS:
            for dataset, param in DATASETS.items():
                url = f"https://www.metoffice.gov.uk/pub/data/weather/uk/climate/datasets/{param}/date/{region}.txt"
                self.stdout.write(f"Fetching {region} - {dataset} from {url}...")
                try:
                    handler = ClimateDataHandler(url, region, dataset)
                    handler.fetch_parse_process()
                    self.stdout.write(
                        self.style.SUCCESS(f"Successfully loaded {dataset}.")
                    )

                except ValueError as e:
                    self.stdout.write(
                        self.style.ERROR(f"Failed to load {dataset}: {str(e)}")
                    )

                except ConnectionError as e:
                    self.stdout.write(
                        self.style.ERROR(
                            f"Connection error while loading {dataset}: {str(e)}"
                        )
                    )
