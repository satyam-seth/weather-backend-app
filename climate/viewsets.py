from rest_framework.viewsets import ReadOnlyModelViewSet

from climate.filters import ClimateRecordFilter
from climate.models import (
    ClimateMonthly,
    ClimateParameter,
    ClimateRecord,
    ClimateRegion,
)
from climate.serializers import (
    ClimateMonthlySerializer,
    ClimateParameterSerializer,
    ClimateRecordSerializer,
    ClimateRegionSerializer,
)


class ClimateRegionViewSet(ReadOnlyModelViewSet):
    """Climate Region ViewSet"""

    queryset = ClimateRegion.objects.all()
    serializer_class = ClimateRegionSerializer


class ClimateParameterViewSet(ReadOnlyModelViewSet):
    """Climate Parameter ViewSet"""

    queryset = ClimateParameter.objects.all()
    serializer_class = ClimateParameterSerializer


class ClimateMonthlyViewSet(ReadOnlyModelViewSet):
    """Climate Monthly ViewSet"""

    queryset = ClimateMonthly.objects.all()
    serializer_class = ClimateMonthlySerializer


class ClimateRecordViewSet(ReadOnlyModelViewSet):  # pylint: disable=too-many-ancestors
    """Climate Record ViewSet"""

    queryset = (
        ClimateRecord.objects.select_related("region", "parameter")
        .all()
        .order_by("year")
    )

    serializer_class = ClimateRecordSerializer
    filterset_class = ClimateRecordFilter
