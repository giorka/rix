from __future__ import annotations

from django.urls import path
from djoser import views as djoser

from . import views

urlpatterns = (
    path('register/', views.UserCreateAPIView.as_view()),
    path('revert/', views.RevertCreateAPIView.as_view()),
    path('revert-complete/', views.RevertCompleteCreateAPIView.as_view()),
    path('verification/', views.EmailVerificationAPIView.as_view()),
    path('verification-complete/', views.EmailVerificationCompleteAPIView.as_view()),
    path('cp/', views.ChangePasswordAPIView.as_view()),
    path('login/', djoser.TokenCreateView.as_view()),
    path('logout/', djoser.TokenDestroyView.as_view()),
)
