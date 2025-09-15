from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class ClimateRegion(models.Model):
    """Climate Region"""

    class Meta:
        indexes = [
            models.Index(fields=["region"]),
        ]
        verbose_name = "Climate Region"
        verbose_name_plural = "Climate Regions"

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

    region = models.CharField(
        max_length=50,
        unique=True,
        choices=Region.choices,
        help_text="Select the geographical region.",
    )

    def __str__(self) -> str:
        return self.get_region_display()


class ClimateParameter(models.Model):
    """Climate Parameter"""

    class Meta:
        indexes = [
            models.Index(fields=["parameter"]),
        ]
        verbose_name = "Climate Parameter"
        verbose_name_plural = "Climate Parameters"

    class Parameter(models.TextChoices):  # pylint: disable=too-many-ancestors
        """Dataset Choices"""

        AIR_FROST = "air_frost", "Air Frost"
        RAIN_DAYS = "raindays", "Rain Days ≥1mm"
        RAINFALL = "rainfall", "Rainfall"
        SUNSHINE = "sunshine", "Sunshine"
        TMEAN = "tmean", "Mean Temperature"
        TMIN = "tmin", "Minimum Temperature"
        TMAX = "tmax", "Maximum Temperature"

    parameter = models.CharField(
        max_length=20,
        choices=Parameter.choices,
        help_text="The type of climate parameter.",
    )

    def __str__(self) -> str:
        return self.get_parameter_display()


class ClimateRecord(models.Model):
    """Climate Record"""

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["parameter", "region", "year"],
                name="unique_parameter_region_year",
            )
        ]
        indexes = [
            models.Index(fields=["region"]),
            models.Index(fields=["parameter"]),
        ]
        verbose_name = "Climate Record"
        verbose_name_plural = "Climate Records"

    region = models.ForeignKey(to=ClimateRegion, on_delete=models.CASCADE)
    parameter = models.ForeignKey(to=ClimateParameter, on_delete=models.CASCADE)
    year = models.PositiveIntegerField(
        help_text="The year this climate data refers to."
    )
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.get_parameter_display()} - {self.region.get_region_display()} - {self.year}"


class ClimateMonthly(models.Model):
    """Climate Monthly Data"""

    class Meta:
        indexes = [
            models.Index(fields=["record", "month"]),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=["record", "month"],
                name="unique_record_month",
            )
        ]
        verbose_name = "Climate Monthly"
        verbose_name_plural = "Climate Monthlies"

    class Month(models.TextChoices):  # pylint: disable=too-many-ancestors
        """Month Choices"""

        JAN = 1, "January"
        FEB = 2, "February"
        MAR = 3, "March"
        APR = 4, "April"
        MAY = 5, "May"
        JUN = 6, "June"
        JUL = 7, "July"
        AUG = 8, "August"
        SEP = 9, "September"
        OCT = 10, "October"
        NOV = 11, "November"
        DEC = 12, "December"

    month = models.PositiveSmallIntegerField(
        choices=Month.choices,
        validators=[MinValueValidator(1), MaxValueValidator(12)],
        help_text="The month of the data, from 1 (January) to 12 (December).",
    )
    data = models.FloatField(null=True, blank=True)
    record = models.ForeignKey(
        to=ClimateRecord,
        on_delete=models.CASCADE,
        related_name="monthly_data",
    )

    def __str__(self):
        return f"{self.record.get_parameter_display()} - {self.record.year} - {self.get_month_display()}"


class ClimateSeason(models.Model):
    """Climate Seasonal Data"""

    class Meta:
        indexes = [
            models.Index(fields=["record", "season"]),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=["season", "record"],
                name="unique_season_record",
            )
        ]
        verbose_name = "Climate Season"
        verbose_name_plural = "Climate Seasons"

    class Season(models.TextChoices):
        """Season Choices"""

        win = "win", "Winter"
        spr = "spr", "Spring"
        sum = "sum", "Summer"
        aut = "aut", "Autumn"
        ann = "ann", "Annual"

    season = models.CharField(
        max_length=3,
        choices=Season.choices,
        help_text="Season for the climate data",
    )
    data = models.FloatField(null=True, blank=True)
    record = models.ForeignKey(
        to=ClimateRecord,
        on_delete=models.CASCADE,
        related_name="season_data",
    )

    def __str__(self):
        return f"{self.get_season_display()} - {self.record.year} - {self.data}"
