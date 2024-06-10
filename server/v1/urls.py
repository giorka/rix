from __future__ import annotations

from django.urls import include
from django.urls import path
from rest_framework import routers

from . import viewsets

router: routers.SimpleRouter = routers.SimpleRouter()

for view_set in viewsets.VIEW_SETS:
    router.register(
        prefix=view_set.Meta.prefix,
        viewset=view_set,
        basename=view_set.Meta.basename,
    )

urlpatterns = (
    path('users/', include('v1__users.urls')),
    *router.urls,
)
