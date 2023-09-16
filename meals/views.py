from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from tablib import Dataset

from .forms import MealUpdateForm, WeeklyMealUploadForm
from .models import Meal, Menu
from .resources import MealResource


def get_active_and_inactive_menus(menu):
    user = menu.user
    menus = Menu.objects.filter(user=user)
    active_menus = menus.filter(active=True)
    inactive_menus = menus.filter(active=False)
    context = {
        "user": user,
        "active_menus": active_menus,
        "inactive_menus": inactive_menus,
    }
    return context


@login_required
def menu_hide(request, menu_id):
    menu = get_object_or_404(Menu, pk=menu_id)
    menu.active = False
    menu.save()
    context = get_active_and_inactive_menus(menu)
    return render(request, "accounts/profile.html#menu_list", context)


@login_required
def menu_publish(request, menu_id):
    menu = get_object_or_404(Menu, pk=menu_id)
    menu.active = True
    menu.save()
    context = get_active_and_inactive_menus(menu)
    return render(request, "accounts/profile.html#menu_list", context)


def get_meals_per_week(menu, week_number):
    return menu.meals.filter(week=week_number)


def get_weeks_choices():
    return [number for number, name in Meal._meta.get_field("week").choices]


def get_days_choices():
    return [number for number, name in Meal._meta.get_field("day").choices]


@login_required
def menu_view(request, menu_id):
    queryset = Menu.objects.prefetch_related("meals")
    menu = get_object_or_404(queryset, pk=menu_id)
    weeks = get_weeks_choices()
    context = {
        "menu": menu,
        "weeks": weeks,
    }
    for week in weeks:
        context["week_" + str(week) + "_meals"] = get_meals_per_week(menu, week)
    return render(request, "meals/menu-view.html", context)


@login_required
def active_weeks(request, menu_id):
    menu = Menu.objects.prefetch_related("meals").get(pk=menu_id)
    weeks_choices = get_weeks_choices()
    weeks = {}
    last_week = 0
    for week in weeks_choices:
        meals_present = menu.meals.filter(week=week).exists()
        weeks.update({week: meals_present})
        if not meals_present:
            break
        last_week += 1
    context = {"menu": menu, "last_week": last_week}
    context["weeks"] = weeks
    return render(request, "meals/includes/weeks.html", context)


@login_required
def menu_weekly_view(request, menu_id, week):
    """Return a view for the meals in the given week, used in Menu View"""
    menu = Menu.objects.prefetch_related("meals").get(pk=menu_id)
    meals_of_the_week = menu.meals.filter(week=week)
    context = {
        "menu": menu,
        "weekly_meals": meals_of_the_week,
        "week": week,
    }
    if request.htmx:
        return render(request, "meals/weekly-menu-view.html#meal_list", context)
    return render(request, "meals/weekly-menu-view.html", context)


@login_required
def add_week_to_menu(request, menu_id, week):
    """Create a complete week of empty meals for the given week, used in Menu View"""
    menu = get_object_or_404(Menu, pk=menu_id)
    days = get_days_choices()
    for day in days:
        Meal.objects.create(menu=menu, week=week, day=day)
    context = get_active_and_inactive_menus(menu)
    return render(request, "accounts/profile.html#menu_list", context)


@login_required
def cancel_week_from_menu(request, menu_id, week):
    """Delete all meals for the given week"""
    menu = get_object_or_404(Menu, pk=menu_id)
    Meal.objects.filter(week=week, menu=menu).delete()
    context = get_active_and_inactive_menus(menu)
    return render(request, "accounts/profile.html#menu_list", context)


@login_required
def meal_update(request, meal_id):
    meal = get_object_or_404(Meal, pk=meal_id)
    if request.method == "POST":
        form = MealUpdateForm(request.POST, instance=meal)
        if form.is_valid():
            form.save()
            return HttpResponse(
                status=204,
                headers={
                    "HX-Trigger": "mealUpdated",
                },
            )
        form = MealUpdateForm(instance=meal)
        context = {
            "form": form,
            "meal": meal,
        }
        return render(request, "meals/meal-update.html", context)
    form = MealUpdateForm(instance=meal)
    context = {
        "form": form,
        "meal": meal,
    }
    return render(request, "meals/meal-update.html", context)


@login_required
def weekly_menu_upload(request, menu_id, week):
    """Take the uploaded file and create/update the meals for the given week"""
    get_object_or_404(Menu, pk=menu_id)
    if request.method == "POST":
        meal_resource = MealResource(menu_id=menu_id, week=week)
        dataset = Dataset()
        form = WeeklyMealUploadForm(
            request.POST, request.FILES, menu_id=menu_id, week=week
        )
        if form.is_valid():
            new_meals = request.FILES["menu"]
            import_data = dataset.load(new_meals.read().decode("utf-8"), format="csv")

            result = meal_resource.import_data(
                import_data, dry_run=False, raise_errors=True
            )

            if not result.has_errors():
                meal_resource.import_data(import_data)
                messages.success(request, "Data imported successfully.")
            else:
                messages.error(request, "There were errors in the import file.")

            return redirect(
                reverse_lazy("meals:menu_weekly_view", args=[menu_id, week])
            )

    upload_form = WeeklyMealUploadForm(menu_id=menu_id, week=week)
    context = {
        "upload_form": upload_form,
        "week": week,
    }
    return render(request, "meals/meal-import.html", context)
