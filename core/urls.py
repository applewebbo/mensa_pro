from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from . import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("allauth.urls")),
    path("accounts/", include("accounts.urls", namespace="accounts")),
    path("__reload__/", include("django_browser_reload.urls")),
    path("", views.index, name="home"),
    path("meals/", include("meals.urls", namespace="meals")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
