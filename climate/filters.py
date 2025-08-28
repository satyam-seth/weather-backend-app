import django_filters

from .models import ClimateRecord


class ClimateRecordFilter(django_filters.FilterSet):
    """Climate Record Filter"""

    dataset = django_filters.CharFilter(field_name="dataset", lookup_expr="iexact")
    year = django_filters.NumberFilter(field_name="year")

    class Meta:
        model = ClimateRecord
        fields = ["dataset", "year"]
