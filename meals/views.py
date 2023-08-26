from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .forms import MenuForm


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
