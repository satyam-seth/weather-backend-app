# tests.py
from unittest.mock import patch

from django.test import TestCase

from climate.models import ClimateRegion


class InvalidateClimateRegionCacheTestCase(TestCase):
    """Test case for ClimateRegion model cache invalidation."""

    @patch("django.core.cache.cache.delete_pattern")
    def test_climate_region_create(self, mock_cache_delete):
        """Test that creating a ClimateRegion invalidates the cache."""

        # Create a new ClimateRegion
        ClimateRegion.objects.create(region=ClimateRegion.Region.UK)

        # Ensure cache.delete_pattern was called
        mock_cache_delete.assert_called_with("*climate_region*")

    @patch("django.core.cache.cache.delete_pattern")
    def test_climate_region_update(self, mock_cache_delete):
        """Test that updating a ClimateRegion invalidates the cache."""

        # Create a new ClimateRegion
        region = ClimateRegion.objects.create(region=ClimateRegion.Region.UK)

        # save to trigger update
        region.save()

        # Ensure cache.delete_pattern was called
        mock_cache_delete.assert_called_with("*climate_region*")

    @patch("django.core.cache.cache.delete_pattern")
    def test_climate_region_delete(self, mock_cache_delete):
        """Test that deleting a ClimateRegion invalidates the cache."""

        # Create a new ClimateRegion
        region = ClimateRegion.objects.create(region=ClimateRegion.Region.UK)

        # Delete the ClimateRegion
        region.delete()

        # Ensure cache.delete_pattern was called
        mock_cache_delete.assert_called_with("*climate_region*")
