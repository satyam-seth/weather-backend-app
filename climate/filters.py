import django_filters

from .models import ClimateRecord


class ClimateRecordFilter(django_filters.FilterSet):
    """Climate Record Filter"""

    dataset = django_filters.ChoiceFilter(
        field_name="dataset",
        choices=ClimateRecord.Dataset.choices,
        lookup_expr="iexact",
    )
    region = django_filters.ChoiceFilter(
        field_name="region",
        choices=ClimateRecord.Region.choices,
        lookup_expr="iexact",
    )
    year = django_filters.NumberFilter(field_name="year")

    class Meta:
        model = ClimateRecord
        fields = ["dataset", "year"]
