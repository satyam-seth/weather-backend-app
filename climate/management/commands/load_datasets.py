from django.core.management.base import BaseCommand

from climate.parser import DATASETS, fetch_and_process_climate_data


class Command(BaseCommand):
    """Management command to load climate datasets"""

    help = "Load Met Office climate datasets"

    def handle(self, *args, **kwargs):
        """Handle command to fetch and parse datasets."""

        for dataset, url in DATASETS.items():
            self.stdout.write(f"Fetching {dataset} from {url}...")
            try:
                fetch_and_process_climate_data(url, dataset)
                self.stdout.write(self.style.SUCCESS(f"Successfully loaded {dataset}."))

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
