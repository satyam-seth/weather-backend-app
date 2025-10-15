from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework.viewsets import ReadOnlyModelViewSet

from climate.filters import ClimateRecordFilter
from climate.models import (
    ClimateMonthly,
    ClimateParameter,
    ClimateRecord,
    ClimateRegion,
    ClimateSeasonal,
)
from climate.serializers import (
    ClimateMonthlySerializer,
    ClimateParameterSerializer,
    ClimateRecordSerializer,
    ClimateRegionSerializer,
    ClimateSeasonalSerializer,
)


class ClimateRegionViewSet(ReadOnlyModelViewSet):
    """Climate Region ViewSet"""

    queryset = ClimateRegion.objects.all()
    serializer_class = ClimateRegionSerializer

    @method_decorator(cache_page(60 * 15, key_prefix="product_retrieve"))
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @method_decorator(cache_page(60 * 15, key_prefix="product_list"))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class ClimateParameterViewSet(ReadOnlyModelViewSet):
    """Climate Parameter ViewSet"""

    queryset = ClimateParameter.objects.all()
    serializer_class = ClimateParameterSerializer


class ClimateMonthlyViewSet(ReadOnlyModelViewSet):
    """Climate Monthly ViewSet"""

    queryset = ClimateMonthly.objects.all()
    serializer_class = ClimateMonthlySerializer


class ClimateSeasonalViewSet(ReadOnlyModelViewSet):
    """Climate Seasonal ViewSet"""

    queryset = ClimateSeasonal.objects.all()
    serializer_class = ClimateSeasonalSerializer


class ClimateRecordViewSet(ReadOnlyModelViewSet):  # pylint: disable=too-many-ancestors
    """Climate Record ViewSet"""

    queryset = (
        ClimateRecord.objects.select_related("region", "parameter")
        .all()
        .order_by("year")
    )

    serializer_class = ClimateRecordSerializer
    filterset_class = ClimateRecordFilter
