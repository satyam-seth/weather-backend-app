import django_filters

from climate.models import ClimateRecord


class ClimateRecordFilter(django_filters.FilterSet):
    """Climate Record Filter"""

    # Filter by region name (FK → ClimateRegion.region)
    region = django_filters.ChoiceFilter(
        field_name="region__region",  # follow FK
        choices=ClimateRecord._meta.get_field("region").related_model.Region.choices,
        lookup_expr="iexact",
    )

    # Filter by parameter (FK → ClimateParameter.parameter)
    parameter = django_filters.ChoiceFilter(
        field_name="parameter__parameter",
        choices=ClimateRecord._meta.get_field(
            "parameter"
        ).related_model.Parameter.choices,
        lookup_expr="iexact",
    )

    # Filter by year
    year = django_filters.NumberFilter(field_name="year")

    class Meta:
        model = ClimateRecord
        fields = ["region", "parameter", "year"]
