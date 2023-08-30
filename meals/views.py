from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render

from .forms import MenuForm
from .models import Meal, Menu


@login_required
def menu_create(request):
    user = request.user
    if request.method == "POST":
        form = MenuForm(request.POST)
        if form.is_valid():
            menu = form.save(commit=False)
            menu.user = user
            menu.save()
    form = MenuForm()
    context = {"form": form}
    return render(request, "meals/menu-create.html", context)


def get_meals_per_week(menu, week_number):
    return menu.meals.filter(week=week_number)


def get_weeks_choices():
    return [number for number, name in Meal._meta.get_field("week").choices]


@login_required
def menu_view(request, pk):
    queryset = Menu.objects.prefetch_related("meals")
    menu = get_object_or_404(queryset, pk=pk)
    weeks = get_weeks_choices()
    context = {
        "menu": menu,
        "weeks": weeks,
    }
    for week in weeks:
        context["week_" + str(week) + "_meals"] = get_meals_per_week(menu, week)
    return render(request, "meals/menu-view.html", context)


@login_required
def single_menu_with_active_weeks(request, pk):
    menu = Menu.objects.prefetch_related("meals").get(pk=pk)
    weeks_choices = get_weeks_choices()
    weeks = {}
    for week in weeks_choices:
        meals_present = menu.meals.filter(week=week).exists()
        weeks.update({week: meals_present})
        if not meals_present:
            break
    context = {"menu": menu}
    context["weeks"] = weeks
    return render(request, "meals/includes/active-weeks.html", context)


@login_required
def menu_weekly_view(request, pk, week):
    menu = Menu.objects.prefetch_related("meals").get(pk=pk)
    meals_of_the_week = menu.meals.filter(week=week)
    context = {
        "menu": menu,
        "weekly_meals": meals_of_the_week,
        "week": week,
    }
    return render(request, "meals/weekly-menu-view.html", context)
