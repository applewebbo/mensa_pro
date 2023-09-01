from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from meals.models import Menu


@login_required
def profile(request):
    user = request.user
    menus = Menu.objects.filter(user=user).prefetch_related("meals")
    active_menus = menus.filter(active=True)
    inactive_menus = menus.filter(active=False)
    context = {
        "user": user,
        "active_menus": active_menus,
        "inactive_menus": inactive_menus,
    }
    return render(request, "accounts/profile.html", context)
