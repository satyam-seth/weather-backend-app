from rest_framework import serializers

from .models import ClimateRecord


class ClimateRecordSerializer(serializers.ModelSerializer):
    """Climate Record Serializer"""

    class Meta:
        model = ClimateRecord
        fields = "__all__"
