from __future__ import annotations

from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from server import settings

urlpatterns = (
    path('admin/', admin.site.urls),
    path('api/v2/', include('v2.urls')),
)

urlpatterns += tuple(
    static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    ),
)
