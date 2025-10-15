from django.conf import settings
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

# TODO: fix it check why is it not working
# class CachedReadOnlyModelViewSet(ReadOnlyModelViewSet):
#     """Base ReadOnlyModelViewSet with caching applied to retrieve and list methods."""

#     cache_timeout = settings.CACHE_TTL

#     def apply_cache_decorator(self):
#         """Applies cache_page decorator to list and retrieve methods."""

#         # print("Applying cache decorators", self.cache_timeout)

#         method_decorator(
#             cache_page(self.cache_timeout, key_prefix=self.get_cache_key_prefix())
#         )(self.list)
#         method_decorator(
#             cache_page(self.cache_timeout, key_prefix=self.get_cache_key_prefix())
#         )(self.retrieve)

#     def get_cache_key_prefix(self):
#         """Override this method in your ViewSet to provide a unique key_prefix."""

#         print("Using cache key prefix", self.__class__.__name__.lower())

#         return self.__class__.__name__.lower()

#     # # To simulate latency for testing caching
#     def get_queryset(self):
#         from time import sleep

#         sleep(2)
#         return super().get_queryset()

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.apply_cache_decorator()


class ClimateRegionViewSet(ReadOnlyModelViewSet):
    """Climate Region ViewSet"""

    queryset = ClimateRegion.objects.all()
    serializer_class = ClimateRegionSerializer

    def get_queryset(self):
        if settings.DEBUG:
            from time import sleep

            sleep(2)
        return super().get_queryset()

    @method_decorator(
        cache_page(settings.CACHE_TTL, key_prefix="climate_region_retrieve")
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @method_decorator(cache_page(settings.CACHE_TTL, key_prefix="climate_region_list"))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class ClimateParameterViewSet(ReadOnlyModelViewSet):
    """Climate Parameter ViewSet"""

    queryset = ClimateParameter.objects.all()
    serializer_class = ClimateParameterSerializer

    def get_queryset(self):
        if settings.DEBUG:
            from time import sleep

            sleep(2)
        return super().get_queryset()

    @method_decorator(
        cache_page(settings.CACHE_TTL, key_prefix="climate_parameter_retrieve")
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @method_decorator(
        cache_page(settings.CACHE_TTL, key_prefix="climate_parameter_list")
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class ClimateMonthlyViewSet(ReadOnlyModelViewSet):
    """Climate Monthly ViewSet"""

    queryset = ClimateMonthly.objects.all()
    serializer_class = ClimateMonthlySerializer

    def get_queryset(self):
        if settings.DEBUG:
            from time import sleep

            sleep(2)
        return super().get_queryset()

    @method_decorator(
        cache_page(settings.CACHE_TTL, key_prefix="climate_monthly_retrieve")
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @method_decorator(cache_page(settings.CACHE_TTL, key_prefix="climate_monthly_list"))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class ClimateSeasonalViewSet(ReadOnlyModelViewSet):
    """Climate Seasonal ViewSet"""

    queryset = ClimateSeasonal.objects.all()
    serializer_class = ClimateSeasonalSerializer

    def get_queryset(self):

        if settings.DEBUG:
            from time import sleep

            sleep(2)
        return super().get_queryset()

    @method_decorator(
        cache_page(settings.CACHE_TTL, key_prefix="climate_seasonal_retrieve")
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @method_decorator(
        cache_page(settings.CACHE_TTL, key_prefix="climate_seasonal_list")
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class ClimateRecordViewSet(ReadOnlyModelViewSet):  # pylint: disable=too-many-ancestors
    """Climate Record ViewSet"""

    queryset = (
        ClimateRecord.objects.select_related("region", "parameter")
        .all()
        .order_by("year")
    )

    serializer_class = ClimateRecordSerializer
    filterset_class = ClimateRecordFilter

    def get_queryset(self):
        if settings.DEBUG:
            from time import sleep

            sleep(2)
        return super().get_queryset()

    @method_decorator(
        cache_page(settings.CACHE_TTL, key_prefix="climate_record_retrieve")
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @method_decorator(cache_page(settings.CACHE_TTL, key_prefix="climate_record_list"))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
