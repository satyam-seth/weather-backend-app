from rest_framework.viewsets import ReadOnlyModelViewSet

from .models import ClimateRecord
from .serializers import ClimateRecordSerializer


class ClimateRecordViewSet(ReadOnlyModelViewSet):
    """Climate Record ViewSet"""

    queryset = ClimateRecord.objects.all()
    serializer_class = ClimateRecordSerializer
