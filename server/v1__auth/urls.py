from typing import Tuple

from django.urls import path
from djoser import views as djoser

from . import views

urlpatterns: Tuple[path, ...] = (
    path('register/', views.RegisterAPIView.as_view()),
    path('device-verification/', views.VerifyAPIView.as_view()),
    path('login/', djoser.TokenCreateView.as_view()),
    path('logout/', djoser.TokenDestroyView.as_view()),

)
