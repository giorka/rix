from __future__ import annotations

from django.urls import path

from . import views

urlpatterns: tuple[path, ...] = (
    path('', views.FileCreateAPIView.as_view()),
    path('<str:username>/<str:pk>/', views.FileRetrieveAPIView.as_view()),
    path(
        '<str:username>/<str:pk>/download/',
        views.FileDownloadAPIView.as_view(),
    ),
)
