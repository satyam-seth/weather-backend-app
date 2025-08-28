from rest_framework.viewsets import ReadOnlyModelViewSet

from climate.filters import ClimateRecordFilter
from climate.models import ClimateRecord
from climate.serializers import ClimateRecordSerializer


class ClimateRecordViewSet(ReadOnlyModelViewSet):  # pylint: disable=too-many-ancestors
    """Climate Record ViewSet"""

    queryset = ClimateRecord.objects.all().order_by("year")
    serializer_class = ClimateRecordSerializer
    filterset_class = ClimateRecordFilter
