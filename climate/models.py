from django.db import models


class ClimateRecord(models.Model):
    """Climate Record"""

    DATASETS = [
        ("air_frost", "Air Frost"),
        ("raindays", "Rain Days ≥1mm"),
        ("rainfall", "Rainfall"),
        ("sunshine", "Sunshine"),
        ("tmean", "Mean Temperature"),
        ("tmin", "Minimum Temperature"),
        ("tmax", "Maximum Temperature"),
    ]

    dataset = models.CharField(max_length=20, choices=DATASETS)
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
                fields=["dataset", "year"], name="unique_dataset_year"
            )
        ]

    def __str__(self):
        return f"{self.get_dataset_display()} - {self.year}"
