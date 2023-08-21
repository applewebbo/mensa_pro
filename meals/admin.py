from django.contrib import admin

from .models import Meal, Menu


@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    search_fields = ["title__istartswith", "user__istartswith"]


@admin.register(Meal)
class MealAdmin(admin.ModelAdmin):
    pass
