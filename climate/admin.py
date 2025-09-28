from django.contrib import admin

from .models import (
    ClimateMonthly,
    ClimateParameter,
    ClimateRecord,
    ClimateRegion,
    ClimateSeason,
)


@admin.register(ClimateRegion)
class ClimateRegionAdmin(admin.ModelAdmin):
    """Climate Region Model Admin"""

    list_display = ("id", "region")


@admin.register(ClimateParameter)
class ClimateParameterAdmin(admin.ModelAdmin):
    """Climate Parameter Model Admin"""

    list_display = ("id", "parameter")
    ordering = ("parameter",)


@admin.register(ClimateRecord)
class ClimateRecordModelAdmin(admin.ModelAdmin):
    """Climate Record Model Admin"""

    list_display = ("id", "year", "region", "parameter", "created_on", "updated_on")
    ordering = ("year", "region")


@admin.register(ClimateMonthly)
class ClimateMonthlyAdmin(admin.ModelAdmin):
    """Climate Monthly Model Admin"""

    list_display = ("id", "month", "data", "record")
    ordering = ("record__year", "month")


@admin.register(ClimateSeason)
class ClimateSeasonAdmin(admin.ModelAdmin):
    """Climate Seasonal Model Admin"""

    list_display = ("id", "season", "data", "record")
    ordering = ("record__year", "season")
