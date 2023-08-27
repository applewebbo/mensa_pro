from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from meals.models import Menu


@login_required
def profile(request):
    user = request.user
    menus = Menu.objects.filter(user=user).prefetch_related("meal_set")
    context = {
        "user": user,
        "menus": menus,
    }
    return render(request, "accounts/profile.html", context)
