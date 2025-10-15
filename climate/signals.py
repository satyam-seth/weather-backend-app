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
def invalidate_climateregion_cache(sender, instance, **kwargs):
    """
    Invalidate climateregion list caches when a climateregion is created, updated, or deleted
    """
    print("Clearing climateregion cache")

    # Clear climateregion list caches
    cache.delete_pattern("*climateregion*")


@receiver([post_save, post_delete], sender=ClimateParameter)
def invalidate_climateparameter_cache(sender, instance, **kwargs):
    """
    Invalidate climateparameter list caches when a climateparameter is created, updated, or deleted
    """
    print("Clearing climateparameter cache")

    # Clear climateparameter list caches
    cache.delete_pattern("*climateparameter*")


@receiver([post_save, post_delete], sender=ClimateSeasonal)
def invalidate_climateseasonal_cache(sender, instance, **kwargs):
    """
    Invalidate climateseasonal list caches when a climateseasonal is created, updated, or deleted
    """
    print("Clearing climateseasonal cache")

    # Clear climateseasonal list caches
    cache.delete_pattern("*climateseasonal*")


@receiver([post_save, post_delete], sender=ClimateRecord)
def invalidate_climaterecord_cache(sender, instance, **kwargs):
    """
    Invalidate climaterecord list caches when a climaterecord is created, updated, or deleted
    """
    print("Clearing climaterecord cache")

    # Clear climaterecord list caches
    cache.delete_pattern("*climaterecord*")


@receiver([post_save, post_delete], sender=ClimateMonthly)
def invalidate_climatemonthly_cache(sender, instance, **kwargs):
    """
    Invalidate climatemonthly list caches when a climatemonthly is created, updated, or deleted
    """
    print("Clearing climatemonthly cache")

    # Clear climatemonthly list caches
    cache.delete_pattern("*climatemonthly*")
