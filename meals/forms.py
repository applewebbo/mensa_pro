from crispy_forms.helper import FormHelper
from django import forms
from django.forms import ModelForm

from .models import Meal, Menu


class MenuForm(ModelForm):
    class Meta:
        model = Menu
        fields = ["type"]

    CHOICES = Menu._meta.get_field("type").choices

    type = forms.ChoiceField(widget=forms.RadioSelect, choices=CHOICES)

    def clean_type(self):
        type = self.cleaned_data["type"]
        user = self.user
        if Menu.objects.filter(user=user, type=type).exists():
            raise forms.ValidationError("Menu type already present in the list")
        return type

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user")
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()


class MealForm(ModelForm):
    class Meta:
        model = Meal
        fields = ["day", "first_course", "second_course", "side_dish", "fruit", "snack"]
