from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from climate import Month, Parameter, Region, Season


class ClimateRegion(models.Model):
    """Climate Region"""

    region = models.CharField(
        max_length=50,
        unique=True,
        choices=Region.choices,
        help_text="Select the geographical region.",
    )

    class Meta:
        indexes = [
            models.Index(fields=["region"]),
        ]

    def __str__(self) -> str:
        return self.get_region_display()


class ClimateParameter(models.Model):
    """Climate Parameter"""

    parameter = models.CharField(
        max_length=20,
        choices=Parameter.choices,
        help_text="The type of climate parameter.",
        unique=True,
    )

    class Meta:
        indexes = [
            models.Index(fields=["parameter"]),
        ]

    def __str__(self) -> str:
        return self.get_parameter_display()


class ClimateRecord(models.Model):
    """Climate Record"""

    region = models.ForeignKey(ClimateRegion, on_delete=models.CASCADE)
    parameter = models.ForeignKey(ClimateParameter, on_delete=models.CASCADE)
    year = models.PositiveIntegerField(
        help_text="The year this climate data refers to.",
        validators=[
            MinValueValidator(1600),
            MaxValueValidator(2100),
        ],
    )
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-year"]
        unique_together = ["parameter", "region", "year"]
        indexes = [
            models.Index(fields=["region"]),
            models.Index(fields=["parameter"]),
        ]

    def __str__(self):
        return f"{self.parameter.get_parameter_display()} - {self.region.get_region_display()} - {self.year}"


class ClimateMonthly(models.Model):
    """Climate Monthly Data"""

    month = models.PositiveSmallIntegerField(
        choices=Month.choices,
        validators=[MinValueValidator(1), MaxValueValidator(12)],
        help_text="The month of the data, from 1 (January) to 12 (December).",
    )
    data = models.FloatField(null=True, blank=True)
    record = models.ForeignKey(ClimateRecord, on_delete=models.CASCADE)

    class Meta:
        indexes = [
            models.Index(fields=["record", "month"]),
        ]
        unique_together = ["record", "month"]

    def __str__(self):
        return f"{self.record.parameter.get_parameter_display()} - {self.record.year} - {self.get_month_display()}"


class ClimateSeasonal(models.Model):
    """Climate Seasonal Data"""

    season = models.CharField(
        max_length=3,
        choices=Season.choices,
        help_text="Season for the climate data",
    )
    data = models.FloatField(null=True, blank=True)
    record = models.ForeignKey(ClimateRecord, on_delete=models.CASCADE)

    class Meta:
        indexes = [
            models.Index(fields=["record", "season"]),
        ]
        unique_together = ["season", "record"]

    def __str__(self):
        return f"{self.get_season_display()} - {self.record.year} - {self.data}"
