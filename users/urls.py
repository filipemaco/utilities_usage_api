from django.urls import path

from rest_framework.routers import SimpleRouter

from .viewsets import UserViewSet

app_name = 'users'

router = SimpleRouter()
router.register('', UserViewSet, basename='users')

urlpatterns = router.urls
