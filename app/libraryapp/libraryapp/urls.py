from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("users.urls", namespace="users")),
    path("", include("catalog.urls", namespace="catalog")),
]
