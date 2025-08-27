from django.test import TestCase
from django.utils import timezone

from .models import ClimateRecord


class ClimateRecordModelTest(TestCase):
    """Climate Record Model Test"""

    def setUp(self):
        """Setup data for tests."""
        self.climate_record = ClimateRecord.objects.create(
            dataset="rainfall",
            year=2023,
            jan=100.5,
            feb=110.2,
            mar=105.7,
            apr=99.3,
            may=120.1,
            jun=115.5,
            jul=110.0,
            aug=125.8,
            sep=105.9,
            oct=99.8,
            nov=103.0,
            dec=108.6,
            win=102.5,
            spr=112.3,
            sum=118.7,
            aut=98.5,
            ann=110.4,
        )

    def test_model_fields(self):
        """Test the fields of the ClimateRecord model."""

        # Test that the object is created successfully
        record = self.climate_record

        # Assert dataset and year
        self.assertEqual(record.dataset, "rainfall")
        self.assertEqual(record.year, 2023)

        # Assert monthly values
        self.assertEqual(record.jan, 100.5)
        self.assertEqual(record.feb, 110.2)
        self.assertEqual(record.mar, 105.7)
        self.assertEqual(record.apr, 99.3)
        self.assertEqual(record.may, 120.1)
        self.assertEqual(record.jun, 115.5)
        self.assertEqual(record.jul, 110.0)
        self.assertEqual(record.aug, 125.8)
        self.assertEqual(record.sep, 105.9)
        self.assertEqual(record.oct, 99.8)
        self.assertEqual(record.nov, 103.0)
        self.assertEqual(record.dec, 108.6)

        # Assert seasonal values
        self.assertEqual(record.win, 102.5)
        self.assertEqual(record.spr, 112.3)
        self.assertEqual(record.sum, 118.7)
        self.assertEqual(record.aut, 98.5)
        self.assertEqual(record.ann, 110.4)

        # Assert timestamps
        self.assertIsInstance(record.created_on, timezone.datetime)
        self.assertIsInstance(record.updated_on, timezone.datetime)

        # Test that created_on is before now
        self.assertLess(record.created_on, timezone.now())

        # Test that updated_on is also set
        self.assertLess(record.updated_on, timezone.now())
