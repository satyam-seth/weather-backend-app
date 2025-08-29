from django.db import models


class ClimateRecord(models.Model):
    """Climate Record"""

    class Dataset(models.TextChoices):  # pylint: disable=too-many-ancestors
        """Dataset Choices"""

        AIR_FROST = "air_frost", "Air Frost"
        RAIN_DAYS = "raindays", "Rain Days ≥1mm"
        RAINFALL = "rainfall", "Rainfall"
        SUNSHINE = "sunshine", "Sunshine"
        TMEAN = "tmean", "Mean Temperature"
        TMIN = "tmin", "Minimum Temperature"
        TMAX = "tmax", "Maximum Temperature"

    class Region(models.TextChoices):  # pylint: disable=too-many-ancestors
        """Region Choices"""

        UK = "UK", "UK"
        ENGLAND = "England", "England"
        WALES = "Wales", "Wales"
        SCOTLAND = "Scotland", "Scotland"
        NORTHERN_IRELAND = "Northern_Ireland", "Northern Ireland"
        ENGLAND_AND_WALES = "England_and_Wales", "England and Wales"
        ENGLAND_N = "England_N", "England North"
        ENGLAND_S = "England_S", "England South"
        SCOTLAND_N = "Scotland_N", "Scotland North"
        SCOTLAND_E = "Scotland_E", "Scotland East"
        SCOTLAND_W = "Scotland_W", "Scotland West"
        ENGLAND_E_AND_NE = "England_E_and_NE", "England East and NE"
        ENGLAND_NW_AND_N_WALES = "England_NW_and_N_Wales", "England NW and North Wales"
        MIDLANDS = "Midlands", "Midlands"
        EAST_ANGLIA = "East_Anglia", "East Anglia"
        ENGLAND_SW_AND_S_WALES = "England_SW_and_S_Wales", "England SW and South Wales"
        ENGLAND_SE_AND_CENTRAL_S = (
            "England_SE_and_Central_S",
            "England SE and Central South",
        )

    dataset = models.CharField(max_length=20, choices=Dataset.choices)
    region = models.CharField(max_length=50, choices=Region.choices)
    year = models.PositiveIntegerField()

    # Monthly values
    jan = models.FloatField(null=True, blank=True)
    feb = models.FloatField(null=True, blank=True)
    mar = models.FloatField(null=True, blank=True)
    apr = models.FloatField(null=True, blank=True)
    may = models.FloatField(null=True, blank=True)
    jun = models.FloatField(null=True, blank=True)
    jul = models.FloatField(null=True, blank=True)
    aug = models.FloatField(null=True, blank=True)
    sep = models.FloatField(null=True, blank=True)
    oct = models.FloatField(null=True, blank=True)
    nov = models.FloatField(null=True, blank=True)
    dec = models.FloatField(null=True, blank=True)

    # Seasonal and annual
    win = models.FloatField(null=True, blank=True)
    spr = models.FloatField(null=True, blank=True)
    sum = models.FloatField(null=True, blank=True)
    aut = models.FloatField(null=True, blank=True)
    ann = models.FloatField(null=True, blank=True)

    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["dataset", "region", "year"],
                name="unique_dataset_region_year",
            )
        ]

    def __str__(self):
        return f"{self.get_dataset_display()} - {self.year}"
