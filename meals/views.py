from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from .forms import MealForm, MenuForm
from .models import Meal, Menu, School


@login_required
def menu_create(request):
    user = request.user
    # TODO: create a path to create a school before menu if school is not present
    school, created = School.objects.get_or_create(user=user)
    if not school.name:
        school.name = "Generic"
        school.save()
    if request.method == "POST":
        form = MenuForm(request.POST)
        if form.is_valid():
            menu = form.save(commit=False)
            menu.user = user
            menu.school = school
            menu.save()
            return redirect(reverse("accounts:profile"))
        form = MenuForm(request.POST)
        context = {"form": form}
        return render(request, "meals/menu-create.html", context)
    form = MenuForm()
    context = {"form": form}
    return render(request, "meals/menu-create.html", context)


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
def menu_delete(request, menu_id):
    menu = get_object_or_404(Menu, pk=menu_id)
    menu.delete()
    context = get_active_and_inactive_menus(menu)
    return render(request, "accounts/profile.html#menu_list", context)


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
def single_menu_with_active_weeks(request, menu_id):
    menu = Menu.objects.prefetch_related("meals").get(pk=menu_id)
    weeks_choices = get_weeks_choices()
    weeks = {}
    for week in weeks_choices:
        meals_present = menu.meals.filter(week=week).exists()
        weeks.update({week: meals_present})
        if not meals_present:
            break
    context = {"menu": menu}
    context["weeks"] = weeks
    return render(request, "meals/includes/weeks.html", context)


@login_required
def menu_weekly_view(request, menu_id, week):
    menu = Menu.objects.prefetch_related("meals").get(pk=menu_id)
    meals_of_the_week = menu.meals.filter(week=week)
    context = {
        "menu": menu,
        "weekly_meals": meals_of_the_week,
        "week": week,
    }
    return render(request, "meals/weekly-menu-view.html", context)


@login_required
def week_meals_create(request, menu_id, week):
    menu = Menu.objects.get(pk=menu_id)
    if request.method == "POST":
        form = MealForm(request.POST)
        if form.is_valid():
            meal = form.save(commit=False)
            meal.menu = menu
            meal.week = week
            meal.save()
            return redirect(reverse("meals:menu_view", args=[menu_id]))
        form = MealForm(request.POST)
        context = {"form": form, "menu": menu, "week": week}
        return render(request, "meals/meal-create.html", context)
    form = MealForm()
    context = {"form": form, "menu": menu, "week": week}
    return render(request, "meals/meal-create.html", context)
