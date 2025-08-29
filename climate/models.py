from django.db import models


class ClimateRecord(models.Model):
    """Climate Record"""

    REGIONS = [
        ("UK", "UK"),
        ("England", "England"),
        ("Wales", "Wales"),
        ("Scotland", "Scotland"),
        ("Northern_Ireland", "Northern Ireland"),
        ("England_and_Wales", "England and Wales"),
        ("England_N", "England North"),
        ("England_S", "England South"),
        ("Scotland_N", "Scotland North"),
        ("Scotland_E", "Scotland East"),
        ("Scotland_W", "Scotland West"),
        ("England_E_and_NE", "England East & NE"),
        ("England_NW_and_N_Wales", "England NW & N Wales"),
        ("Midlands", "Midlands"),
        ("East_Anglia", "East Anglia"),
        ("England_SW_and_S_Wales", "England SW & S Wales"),
        ("England_SE_and_Central_S", "England SE & Central South"),
    ]

    DATASETS = [
        ("air_frost", "Air Frost"),
        ("raindays", "Rain Days ≥1mm"),
        ("rainfall", "Rainfall"),
        ("sunshine", "Sunshine"),
        ("tmean", "Mean Temperature"),
        ("tmin", "Minimum Temperature"),
        ("tmax", "Maximum Temperature"),
    ]

    region = models.CharField(max_length=40, choices=REGIONS)
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
                fields=["dataset", "region", "year"],
                name="unique_dataset_region_year",
            )
        ]

    def __str__(self):
        return f"{self.get_dataset_display()} - {self.year}"
