from django.contrib import admin

from .models import Meal, Menu, School


@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    search_fields = ["user__istartswith"]


@admin.register(Meal)
class MealAdmin(admin.ModelAdmin):
    list_display = ["menu", "get_menu_type", "day", "week"]

    @admin.display(description="Menu Type", ordering="menu__type")
    def get_menu_type(self, obj):
        return obj.menu.get_type_display()


@admin.register(School)
class SchoolAdmin(admin.ModelAdmin):
    pass
