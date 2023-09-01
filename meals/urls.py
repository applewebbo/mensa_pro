from django.urls import path

from . import views

app_name = "meals"

urlpatterns = [
    path("menu-create/", views.menu_create, name="menu_create"),
    path("menu/<int:menu_id>", views.menu_view, name="menu_view"),
    path(
        "menu/<int:menu_id>/<int:week>", views.menu_weekly_view, name="menu_weekly_view"
    ),
]

htmx_urlpatterns = [
    path(
        "menu-weeks/<int:menu_id>",
        views.single_menu_with_active_weeks,
        name="menu_weeks_view",
    ),
    path(
        "meal-week/<int:menu_id>/<int:week>",
        views.week_meals_create,
        name="week_meals_create",
    ),
    path("menu-delete/<int:menu_id>", views.menu_delete, name="menu_delete"),
    path("menu-hide/<int:menu_id>", views.menu_hide, name="menu_hide"),
    path("menu-publish/<int:menu_id>", views.menu_publish, name="menu_publish"),
]

urlpatterns += htmx_urlpatterns
