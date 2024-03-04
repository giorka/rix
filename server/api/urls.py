from django.urls import path
from . import views

auth_urlpatterns = (
    path('register/', views.RegisterAPIView.as_view()),

)

urlpatterns = (
    *auth_urlpatterns,
)
