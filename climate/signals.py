from django.core.cache import cache
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from climate.models import (
    ClimateMonthly,
    ClimateParameter,
    ClimateRecord,
    ClimateRegion,
    ClimateSeasonal,
)


@receiver([post_save, post_delete], sender=ClimateRegion)
def invalidate_climate_region_cache(sender, instance, **kwargs):
    """
    Invalidate climate_region list caches when a climate_region is created, updated, or deleted
    """
    # print("Clearing climate_region cache")

    # Clear climate_region list caches
    cache.delete_pattern("*climate_region*")


@receiver([post_save, post_delete], sender=ClimateParameter)
def invalidate_climate_parameter_cache(sender, instance, **kwargs):
    """
    Invalidate climate_parameter list caches when a climate_parameter is created, updated, or deleted
    """
    # print("Clearing climate_parameter cache")

    # Clear climate_parameter list caches
    cache.delete_pattern("*climate_parameter*")


@receiver([post_save, post_delete], sender=ClimateSeasonal)
def invalidate_climate_seasonal_cache(sender, instance, **kwargs):
    """
    Invalidate climate_seasonal list caches when a climate_seasonal is created, updated, or deleted
    """
    # print("Clearing climate_seasonal cache")

    # Clear climate_seasonal list caches
    cache.delete_pattern("*climate_seasonal*")


@receiver([post_save, post_delete], sender=ClimateRecord)
def invalidate_climate_record_cache(sender, instance, **kwargs):
    """
    Invalidate climate_record list caches when a climate_record is created, updated, or deleted
    """
    # print("Clearing climate_record cache")

    # Clear climate_record list caches
    cache.delete_pattern("*climate_record*")


@receiver([post_save, post_delete], sender=ClimateMonthly)
def invalidate_climate_monthly_cache(sender, instance, **kwargs):
    """
    Invalidate climate_monthly list caches when a climate_monthly is created, updated, or deleted
    """
    # print("Clearing climate_monthly cache")

    # Clear climate_monthly list caches
    cache.delete_pattern("*climate_monthly*")
