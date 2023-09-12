from crispy_forms.helper import FormHelper
from crispy_forms.layout import Field, Layout
from django import forms

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
        self.helper.form_class = "form-horizontal"
        self.helper.form_tag = False
        self.helper.label_class = "col-4 text-muted fw-light"
        self.helper.field_class = "col-8"
        self.helper.layout = Layout(
            Field("first_course", css_class="form-control-sm"),
            Field("second_course", css_class="form-control-sm"),
            Field("side_dish", css_class="form-control-sm"),
            Field("fruit", css_class="form-control-sm"),
            Field("snack", css_class="form-control-sm"),
        )
