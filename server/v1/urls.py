from django.urls import include, path
from rest_framework import routers

from . import viewsets

# TODO: for
router: routers.SimpleRouter = routers.SimpleRouter()
router.register(prefix='files', viewset=viewsets.PersonViewSet, basename='files')

urlpatterns = (
    *router.urls,
    path('auth/', include('v1__auth.urls')),
)
