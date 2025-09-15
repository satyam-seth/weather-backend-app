from django.db import IntegrityError
from django.test import TestCase
from django.utils import timezone

from .models import ClimateParameter, ClimateRecord, ClimateRegion


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


class ClimateRegionModelTest(TestCase):
    """Climate Region Model Test"""

    def test_model_fields(self):
        """Test the fields of the ClimateRecord model."""

        record = ClimateRegion.objects.create(region=ClimateRegion.Region.UK)
        # Test that the object is created successfully
        self.assertEqual(ClimateRegion.Region.UK, record.region)
