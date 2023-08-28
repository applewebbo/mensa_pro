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


@login_required
def menu_view(request, pk):
    queryset = Menu.objects.prefetch_related("meals")
    menu = get_object_or_404(queryset, pk=pk)
    weeks = [number for number, name in Meal._meta.get_field("week").choices]
    context = {"menu": menu, "weeks": weeks}
    for week in weeks:
        context["week_" + str(week) + "_meals"] = get_meals_per_week(menu, week)
    return render(request, "meals/menu-view.html", context)
