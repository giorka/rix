from __future__ import annotations

from django.urls import path

from . import views

urlpatterns: tuple[path, ...] = (
    path('me/', views.UserDetailsRetrieveAPIView.as_view()),
    path('<str:username>/', views.UserRetrieveAPIView.as_view()),
)
