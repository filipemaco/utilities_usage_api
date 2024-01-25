from django.urls import path
from rest_framework.routers import SimpleRouter

from .viewsets import UsageViewSet, UsageTypeViewSet

app_name = 'usage'

router = SimpleRouter()
router.register('types', UsageTypeViewSet, basename='usage_types')
router.register('', UsageViewSet, basename='usages')

urlpatterns = router.urls
