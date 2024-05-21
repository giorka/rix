from __future__ import annotations

from django.urls import path
from djoser import views as djoser

from . import views

urlpatterns: tuple[path, ...] = (
    path('register/', views.UserCreateAPIView.as_view()),
    path('session/', views.SessionAPIView.as_view()),
    path('email-verification/', views.EmailVerificationAPIView.as_view()),
    path('login/', djoser.TokenCreateView.as_view()),
    path('logout/', djoser.TokenDestroyView.as_view()),
)
