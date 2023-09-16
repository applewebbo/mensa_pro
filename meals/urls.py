from django.urls import path

from . import views

app_name = "meals"

urlpatterns = [
    path("menu/<int:menu_id>", views.menu_view, name="menu_view"),
    path(
        "menu/<int:menu_id>/<int:week>", views.menu_weekly_view, name="menu_weekly_view"
    ),
]

htmx_urlpatterns = [
    path("week-add/<int:menu_id>/<int:week>", views.add_week_to_menu, name="week_add"),
    path(
        "week-cancel/<int:menu_id>/<int:week>",
        views.cancel_week_from_menu,
        name="week_cancel",
    ),
    path("menu-weeks/<int:menu_id>", views.active_weeks, name="menu_active_weeks"),
    path("menu-hide/<int:menu_id>", views.menu_hide, name="menu_hide"),
    path("menu-publish/<int:menu_id>", views.menu_publish, name="menu_publish"),
    path("meal-update/<int:meal_id>", views.meal_update, name="meal_update"),
    path(
        "week-upload/<int:menu_id>/<int:week>",
        views.weekly_menu_upload,
        name="week_upload",
    ),
]

urlpatterns += htmx_urlpatterns
