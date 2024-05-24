from __future__ import annotations

from django.urls import path

from . import views

urlpatterns: tuple[path, ...] = (
    path('', views.FileCreateAPIView.as_view()),
)
