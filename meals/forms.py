from crispy_bootstrap5.bootstrap5 import FloatingField
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Div, Field, Layout, Submit
from django import forms
from django.urls import reverse_lazy

from .models import Meal, Menu, School


class MenuForm(forms.ModelForm):
    class Meta:
        model = Menu
        fields = ["type"]

    CHOICES = Menu._meta.get_field("type").choices

    type = forms.ChoiceField(widget=forms.RadioSelect, choices=CHOICES)

    # def clean_type(self):
    #     type = self.cleaned_data["type"]
    #     user = self.user
    #     if Menu.objects.filter(user=user, type=type).exists():
    #         raise forms.ValidationError("Menu type already present in the list")
    #     return type

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user")
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()


class SchoolForm(forms.ModelForm):
    class Meta:
        model = School
        fields = ["name"]


class MealUpdateForm(forms.ModelForm):
    class Meta:
        model = Meal
        fields = ["first_course", "second_course", "side_dish", "fruit", "snack"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            FloatingField("first_course"),
            FloatingField("second_course"),
            FloatingField("side_dish"),
            FloatingField("fruit"),
            FloatingField("snack"),
        )


class WeeklyMealUploadForm(forms.Form):
    menu = forms.FileField()

    def __init__(self, *args, **kwargs):
        self.menu_id = kwargs.pop("menu_id")
        self.week = kwargs.pop("week")
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False
        self.helper.form_action = reverse_lazy(
            "meals:week_upload", args=[self.menu_id, self.week]
        )
        # self.helper.disable_csrf = True
        self.helper.layout = Layout(
            Field("menu", accept=".csv"),
            Div(
                Submit("submit", "Save"),
                Submit(
                    "button",
                    "Cancel",
                    css_class="btn btn-danger",
                    data_bs_dismiss="modal",
                ),
                css_class="text-end",
            ),
        )
