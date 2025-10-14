from rest_framework.routers import DefaultRouter

from climate import viewsets

climate_router = DefaultRouter()
climate_router.register("regions", viewsets.ClimateRegionViewSet, basename="regions")
climate_router.register("climate", viewsets.ClimateRecordViewSet, basename="climate")
