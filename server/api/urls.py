from django.urls import path
from . import views

auth_urlpatterns = (
    path('v1/verify/', views.VerifyAPIView.as_view()),
    path('v1/register/', views.RegisterAPIView.as_view()),

)

urlpatterns = (
    *auth_urlpatterns,
)
