from rest_framework import serializers

from .models import ClimateParameter, ClimateRecord, ClimateRegion


class ClimateRegionSerializer(serializers.ModelSerializer):
    """Climate Region Serializer"""

    class Meta:
        model = ClimateRegion
        fields = "__all__"


class ClimateParameterSerializer(serializers.ModelSerializer):
    """Climate Parameter Serializer"""

    class Meta:
        model = ClimateParameter
        fields = "__all__"


class ClimateRecordSerializer(serializers.ModelSerializer):
    """Climate Record Serializer"""

    class Meta:
        model = ClimateRecord
        fields = "__all__"
