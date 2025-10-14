from rest_framework import serializers

from .models import (
    ClimateMonthly,
    ClimateParameter,
    ClimateRecord,
    ClimateRegion,
    ClimateSeasonal,
)


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


class ClimateMonthlySerializer(serializers.ModelSerializer):
    """Climate Monthly Serializer"""

    class Meta:
        model = ClimateMonthly
        fields = "__all__"


class ClimateSeasonalSerializer(serializers.ModelSerializer):
    """Climate Seasonal Serializer"""

    class Meta:
        model = ClimateSeasonal
        fields = "__all__"


class ClimateRecordSerializer(serializers.ModelSerializer):
    """Climate Record Serializer"""

    class Meta:
        model = ClimateRecord
        fields = "__all__"
