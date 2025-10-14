from rest_framework.routers import DefaultRouter

from climate import viewsets

climate_router = DefaultRouter()
climate_router.register(
    "regions",
    viewsets.ClimateRegionViewSet,
    basename="regions",
)
climate_router.register(
    "parameters",
    viewsets.ClimateParameterViewSet,
    basename="parameters",
)
climate_router.register(
    "monthly",
    viewsets.ClimateMonthlyViewSet,
    basename="monthly",
)
climate_router.register(
    "seasonal",
    viewsets.ClimateMonthlyViewSet,
    basename="seasonal",
)
climate_router.register(
    "climate",
    viewsets.ClimateRecordViewSet,
    basename="climate",
)
