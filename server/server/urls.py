from django.contrib import admin
from django.urls import path, include

urlpatterns = (
    path('admin/', admin.site.urls),
    path('api/v1/auth/', include('v1__auth.urls')),
    path('api/v1/', include('v1.urls')),

)
