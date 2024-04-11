from __future__ import annotations

from django.urls import include
from django.urls import path
from rest_framework import routers

from . import viewsets

router: routers.SimpleRouter = routers.SimpleRouter()

for view_set in viewsets.VIEW_SETS:
    router.register(
        prefix=view_set.Meta.prefix,
        viewset=viewsets.PersonViewSet,
        basename=view_set.Meta.basename,
    )

urlpatterns: tuple[path, ...] = (
    *router.urls,
    path('auth/', include('v1__auth.urls')),
    path('users/', include('v1__users.urls')),
)
