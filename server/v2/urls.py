from __future__ import annotations

from django.urls import include
from django.urls import path

urlpatterns = (
    path('auth/', include('v2__auth.urls')),
    path('files/', include('v2__files.urls')),
)
