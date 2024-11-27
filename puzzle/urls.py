"""
URL configuration
"""

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    # Debug only, django reload
    path("__reload__/", include("django_browser_reload.urls")),
]
