from django.urls import path

from . import views

app_name = "meals"

urlpatterns = [
    path("menu-create/", views.menu_create, name="menu_create"),
]
