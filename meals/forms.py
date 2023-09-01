from django.forms import ModelForm

from .models import Meal, Menu


class MenuForm(ModelForm):
    class Meta:
        model = Menu
        fields = ["type"]


class MealForm(ModelForm):
    class Meta:
        model = Meal
        fields = ["day", "first_course", "second_course", "side_dish", "fruit", "snack"]
