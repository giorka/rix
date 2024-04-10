from typing import Tuple

from django.urls import path

from . import views

urlpatterns: Tuple[path, ...] = (
    path('me/', views.ProfileRetrieveAPIView.as_view()),
    path('<str:username>/', views.UserRetrieveAPIView.as_view()),
)