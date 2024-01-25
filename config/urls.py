from django.contrib import admin
from django.urls import include, path

from rest_framework import permissions
from rest_framework.schemas import get_schema_view

from dj_rest_auth.views import LoginView, LogoutView, UserDetailsView

from utils.permissions import IsAdminUser

urlpatterns = [
   path('admin/', admin.site.urls),
   path('api/v1/users/', include('users.urls')),
   path('api/v1/usages/', include('usages.urls')),
   path('api/v1/login/', LoginView.as_view(), name='login'),
   path('api/v1/logout/', LogoutView.as_view(), name='logout'),
   path(
      'openapi',
      get_schema_view(
         title="Utilities API",
         version="1.0.0",
         description='This service is responsible for the usage of each user, \
            usages types, users edition and authentication',
         permission_classes=[IsAdminUser]
      ),
      name='openapi-schema'
   )
]
