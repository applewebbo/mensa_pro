from django.urls import path

from . import views

app_name = "meals"

urlpatterns = [
    path("menu-create/", views.menu_create, name="menu_create"),
    path("menu/<int:pk>", views.menu_view, name="menu_view"),
    path("menu/<int:pk>/<int:week>", views.menu_weekly_view, name="menu_weekly_view"),
]

htmx_urlpatterns = [
    path(
        "menu-weeks/<int:pk>",
        views.single_menu_with_active_weeks,
        name="menu_weeks_view",
    ),
]

urlpatterns += htmx_urlpatterns
