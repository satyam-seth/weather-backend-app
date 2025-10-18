import django_filters

from climate import Parameter, Region
from climate.models import ClimateRecord


class ClimateRecordFilter(django_filters.FilterSet):
    """Climate Record Filter"""

    # Filter by region name (FK → ClimateRegion.region)
    region = django_filters.ChoiceFilter(
        field_name="region__region",  # follow FK
        choices=Region.choices,
        lookup_expr="iexact",
    )

    # Filter by parameter (FK → ClimateParameter.parameter)
    parameter = django_filters.ChoiceFilter(
        field_name="parameter__parameter",
        choices=Parameter.choices,
        lookup_expr="iexact",
    )

    # Filter by year
    year = django_filters.NumberFilter(field_name="year")

    class Meta:
        model = ClimateRecord
        fields = ["region", "parameter", "year"]
