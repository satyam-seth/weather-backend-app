from django.core.management.base import BaseCommand

from climate.parser import DATASETS, REGIONS, fetch_and_process_climate_data


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
                    fetch_and_process_climate_data(url, region, dataset)
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
