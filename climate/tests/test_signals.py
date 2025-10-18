from unittest.mock import patch

from django.test import TestCase

from climate import Parameter, Region, Season
from climate.models import (
    ClimateMonthly,
    ClimateParameter,
    ClimateRecord,
    ClimateRegion,
    ClimateSeasonal,
)


class InvalidateClimateRegionCacheTestCase(TestCase):
    """Test case for ClimateRegion model cache invalidation."""

    @patch("django.core.cache.cache.delete_pattern")
    def test_climate_region_create(self, mock_cache_delete):
        """Test that creating a ClimateRegion invalidates the cache."""

        # Create a new ClimateRegion
        ClimateRegion.objects.create(region=Region.UK)

        # Ensure cache.delete_pattern was called
        mock_cache_delete.assert_called_with("*climate_region*")

    @patch("django.core.cache.cache.delete_pattern")
    def test_climate_region_update(self, mock_cache_delete):
        """Test that updating a ClimateRegion invalidates the cache."""

        # Create a new ClimateRegion
        region = ClimateRegion.objects.create(region=Region.WALES)

        # Trigger an update
        region.region = Region.SCOTLAND
        region.save()

        # Ensure cache.delete_pattern was called
        mock_cache_delete.assert_called_with("*climate_region*")

    @patch("django.core.cache.cache.delete_pattern")
    def test_climate_region_delete(self, mock_cache_delete):
        """Test that deleting a ClimateRegion invalidates the cache."""

        # Create a new ClimateRegion
        region = ClimateRegion.objects.create(region=Region.ENGLAND)

        # Delete the ClimateRegion
        region.delete()

        # Ensure cache.delete_pattern was called
        mock_cache_delete.assert_called_with("*climate_region*")


class InvalidateClimateParameterCacheTestCase(TestCase):
    """Test case for ClimateParameter model cache invalidation."""

    @patch("django.core.cache.cache.delete_pattern")
    def test_climate_parameter_create(self, mock_cache_delete):
        """Test that creating a ClimateParameter invalidates the cache."""

        # Create a new ClimateParameter
        ClimateParameter.objects.create(parameter=Parameter.RAINFALL)

        # Ensure cache.delete_pattern was called with the correct pattern
        mock_cache_delete.assert_called_with("*climate_parameter*")

    @patch("django.core.cache.cache.delete_pattern")
    def test_climate_parameter_update(self, mock_cache_delete):
        """Test that updating a ClimateParameter invalidates the cache."""

        # Create a new ClimateParameter
        param = ClimateParameter.objects.create(parameter=Parameter.SUNSHINE)

        # save to trigger update
        param.parameter = Parameter.TMAX
        param.save()

        # Ensure cache.delete_pattern was called with the correct pattern
        mock_cache_delete.assert_called_with("*climate_parameter*")

    @patch("django.core.cache.cache.delete_pattern")
    def test_climate_parameter_delete(self, mock_cache_delete):
        """Test that deleting a ClimateParameter invalidates the cache."""

        # Create a new ClimateParameter
        param = ClimateParameter.objects.create(parameter=Parameter.RAIN_DAYS)

        # Delete the ClimateParameter
        param.delete()

        # Ensure cache.delete_pattern was called with the correct pattern
        mock_cache_delete.assert_called_with("*climate_parameter*")


class InvalidateClimateSeasonalCacheTestCase(TestCase):
    """Test case for ClimateSeasonal model cache invalidation."""

    def setUp(self):
        self.region = ClimateRegion.objects.create(region=Region.UK)
        self.parameter = ClimateParameter.objects.create(
            parameter=Parameter.RAINFALL,
        )
        self.record = ClimateRecord.objects.create(
            region=self.region,
            parameter=self.parameter,
            year=2020,
        )

    @patch("django.core.cache.cache.delete_pattern")
    def test_climate_seasonal_create(self, mock_cache_delete):
        """Test that creating a ClimateSeasonal invalidates the cache."""

        # Create a new ClimateSeasonal
        ClimateSeasonal.objects.create(
            season=Season.WIN,
            data=12.5,
            record=self.record,
        )

        # Ensure cache.delete_pattern was called with the correct pattern
        mock_cache_delete.assert_called_with("*climate_seasonal*")

    @patch("django.core.cache.cache.delete_pattern")
    def test_climate_seasonal_update(self, mock_cache_delete):
        """Test that updating a ClimateSeasonal invalidates the cache."""

        # Create a new ClimateSeasonal
        seasonal = ClimateSeasonal.objects.create(
            season=Season.WIN,
            data=12.5,
            record=self.record,
        )

        # Trigger an update
        seasonal.data = 15.0
        seasonal.save()

        # Ensure cache.delete_pattern was called with the correct pattern
        mock_cache_delete.assert_called_with("*climate_seasonal*")

    @patch("django.core.cache.cache.delete_pattern")
    def test_climate_seasonal_delete(self, mock_cache_delete):
        """Test that deleting a ClimateSeasonal invalidates the cache."""

        # Create a new ClimateSeasonal
        seasonal = ClimateSeasonal.objects.create(
            season=Season.ANN,
            data=12.5,
            record=self.record,
        )

        # Delete the ClimateSeasonal instance
        seasonal.delete()

        # Ensure cache.delete_pattern was called with the correct pattern
        mock_cache_delete.assert_called_with("*climate_seasonal*")


class InvalidateClimateRecordCacheTestCase(TestCase):
    """Test case for ClimateRecord model cache invalidation."""

    def setUp(self):
        """Setup data for tests."""

        self.region = ClimateRegion.objects.create(region=Region.UK)
        self.parameter = ClimateParameter.objects.create(parameter=Parameter.RAINFALL)

    @patch("django.core.cache.cache.delete_pattern")
    def test_climate_record_create(self, mock_cache_delete):
        """Test that creating a ClimateRecord invalidates the cache."""

        # Create a new ClimateRecord
        ClimateRecord.objects.create(
            region=self.region,
            parameter=self.parameter,
            year=2023,
        )

        # Ensure cache.delete_pattern was called
        mock_cache_delete.assert_called_with("*climate_record*")

    @patch("django.core.cache.cache.delete_pattern")
    def test_climate_record_update(self, mock_cache_delete):
        """Test that updating a ClimateRecord invalidates the cache."""

        # Create a new ClimateRecord
        record = ClimateRecord.objects.create(
            region=self.region,
            parameter=self.parameter,
            year=2021,
        )

        # Trigger an update
        record.year = 2001
        record.save()

        # Ensure cache.delete_pattern was called
        mock_cache_delete.assert_called_with("*climate_record*")

    @patch("django.core.cache.cache.delete_pattern")
    def test_climate_record_delete(self, mock_cache_delete):
        """Test that deleting a ClimateRecord invalidates the cache."""

        # Create a new ClimateRecord
        record = ClimateRecord.objects.create(
            region=self.region,
            parameter=self.parameter,
            year=2020,
        )

        # Delete the record
        record.delete()

        # Ensure cache.delete_pattern was called
        mock_cache_delete.assert_called_with("*climate_record*")


class InvalidateClimateMonthlyCacheTestCase(TestCase):
    """Test case for ClimateMonthly model cache invalidation."""

    def setUp(self):
        self.region = ClimateRegion.objects.create(region=Region.UK)
        self.parameter = ClimateParameter.objects.create(parameter=Parameter.RAINFALL)
        self.record = ClimateRecord.objects.create(
            region=self.region,
            parameter=self.parameter,
            year=2023,
        )

    @patch("django.core.cache.cache.delete_pattern")
    def test_climate_monthly_create(self, mock_cache_delete):
        """Test that creating a ClimateMonthly invalidates the cache."""

        # Create a new ClimateMonthly
        ClimateMonthly.objects.create(record=self.record, month=1, data=25.3)

        # Ensure cache.delete_pattern was called
        mock_cache_delete.assert_called_with("*climate_monthly*")

    @patch("django.core.cache.cache.delete_pattern")
    def test_climate_monthly_update(self, mock_cache_delete):
        """Test that updating a ClimateMonthly invalidates the cache."""

        # Create a new ClimateMonthly
        monthly = ClimateMonthly.objects.create(record=self.record, month=2, data=10.5)

        # Update and save the instance
        monthly.data = 30.0
        monthly.save()

        # Ensure cache.delete_pattern was called
        mock_cache_delete.assert_called_with("*climate_monthly*")

    @patch("django.core.cache.cache.delete_pattern")
    def test_climate_monthly_delete(self, mock_cache_delete):
        """Test that deleting a ClimateMonthly invalidates the cache."""

        # Create a new ClimateMonthly
        monthly = ClimateMonthly.objects.create(record=self.record, month=3, data=25.3)

        # Delete the instance
        monthly.delete()

        # Ensure cache.delete_pattern was called
        mock_cache_delete.assert_called_with("*climate_monthly*")
