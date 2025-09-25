from django.db import IntegrityError
from django.test import TestCase
from django.utils import timezone

from .models import ClimateMonthly, ClimateParameter, ClimateRecord, ClimateRegion


class ClimateRecordModelTest(TestCase):
    """Climate Record Model Test"""

    def setUp(self):
        """Setup data for tests."""

        self.region = ClimateRegion.objects.create(region=ClimateRegion.Region.UK)
        self.parameter = ClimateParameter.objects.create(
            parameter=ClimateParameter.Parameter.RAINFALL
        )
        self.climate_record = ClimateRecord.objects.create(
            region=self.region,
            parameter=self.parameter,
            year=2023,
        )

    def test_model_fields(self):
        """Test the fields of the ClimateRecord model."""

        # Test that the object is created successfully
        record = self.climate_record
        self.assertEqual(record.region, self.region)
        self.assertEqual(record.parameter, self.parameter)
        self.assertEqual(record.year, 2023)

        # Assert timestamps
        self.assertIsInstance(record.created_on, timezone.datetime)
        self.assertIsInstance(record.updated_on, timezone.datetime)

        # Test that created_on is before now
        self.assertLess(record.created_on, timezone.now())

        # Test that updated_on is also set
        self.assertLess(record.updated_on, timezone.now())

    def test_unique_together_constraint(self):
        """Test the unique_together constraint on region, parameter and year."""

        # Try to create a duplicate record (same region, parameter and year)
        with self.assertRaises(IntegrityError):
            ClimateRecord.objects.create(
                region=self.region,
                parameter=self.parameter,
                year=2023,
            )

    def test_str_representation(self):
        """Test the string representation of the ClimateRecord model."""

        record = self.climate_record
        expected_str = "Rainfall - UK - 2023"
        self.assertEqual(str(record), expected_str)


class ClimateRegionModelTest(TestCase):
    """Climate Region Model Test"""

    def test_model_fields(self):
        """Test the fields of the ClimateRecord model."""

        record = ClimateRegion.objects.create(region=ClimateRegion.Region.UK)
        # Test that the object is created successfully
        self.assertEqual(ClimateRegion.Region.UK, record.region)

    def test_str_representation(self):
        """Test the string representation of the ClimateRegion model."""

        record = ClimateRegion.objects.create(region=ClimateRegion.Region.UK)
        expected_str = "UK"
        self.assertEqual(str(record), expected_str)


class ClimateParameterModelTest(TestCase):
    """Climate Parameter Model Test"""

    def test_model_fields(self):
        """Test the fields of the ClimateParameter model."""

        record = ClimateParameter.objects.create(
            parameter=ClimateParameter.Parameter.RAINFALL
        )
        # Test that the object is created successfully
        self.assertEqual(ClimateParameter.Parameter.RAINFALL, record.parameter)

    def test_str_representation(self):
        """Test the string representation of the ClimateParameter model."""

        record = ClimateParameter.objects.create(
            parameter=ClimateParameter.Parameter.RAINFALL
        )
        expected_str = "Rainfall"
        self.assertEqual(str(record), expected_str)


class ClimateMonthlyModelTest(TestCase):
    """Climate Monthly Model Test"""

    def setUp(self):
        self.region = ClimateRegion.objects.create(region=ClimateRegion.Region.UK)
        self.parameter = ClimateParameter.objects.create(
            parameter=ClimateParameter.Parameter.RAINFALL
        )
        self.record = ClimateRecord.objects.create(
            region=self.region,
            parameter=self.parameter,
            year=2023,
        )

    def test_create_valid_climate_monthly(self):
        """Test creating a valid ClimateMonthly instance."""

        monthly = ClimateMonthly.objects.create(record=self.record, month=1, data=25.3)
        self.assertEqual(monthly.month, 1)
        self.assertEqual(monthly.data, 25.3)
        self.assertEqual(monthly.record, self.record)

    def test_get_month_display(self):
        """Test the get_month_display method."""

        monthly = ClimateMonthly.objects.create(record=self.record, month=3, data=12.3)

        expected_str = "Rainfall - 2023 - March"
        self.assertEqual(str(monthly), expected_str)
