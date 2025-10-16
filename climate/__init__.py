from django.db import models


class Region(models.TextChoices):
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


class Parameter(models.TextChoices):
    """Dataset Choices"""

    AIR_FROST = "air_frost", "Air Frost"
    RAIN_DAYS = "raindays", "Rain Days ≥1mm"
    RAINFALL = "rainfall", "Rainfall"
    SUNSHINE = "sunshine", "Sunshine"
    TMEAN = "tmean", "Mean Temperature"
    TMIN = "tmin", "Minimum Temperature"
    TMAX = "tmax", "Maximum Temperature"


class Month(models.IntegerChoices):
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


class Season(models.TextChoices):
    """Season Choices"""

    WIN = "win", "Winter"
    SPR = "spr", "Spring"
    SUM = "sum", "Summer"
    AUT = "aut", "Autumn"
    ANN = "ann", "Annual"
