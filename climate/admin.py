from django.contrib import admin

from .models import ClimateRecord


@admin.register(ClimateRecord)
class ClimateRecordModelAdmin(admin.ModelAdmin):
    """Climate Record Model Admin"""

    list_display = (
        "id",
        "year",
        "dataset",
        "jan",
        "feb",
        "mar",
        "apr",
        "may",
        "jun",
        "jul",
        "aug",
        "sep",
        "oct",
        "nov",
        "dec",
        "win",
        "spr",
        "sum",
        "aut",
        "ann",
        "created_on",
        "updated_on",
    )
