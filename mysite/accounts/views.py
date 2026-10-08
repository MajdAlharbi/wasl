from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from .forms import VisitorProfileForm
from .models import VisitorProfile


@login_required
def index(request):
    return render(request, "accounts/index.html")


def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("accounts:login")
    else:
        form = UserCreationForm()

    return render(request, "accounts/register.html", {"form": form})


@login_required
def preferences(request):
    profile, _ = VisitorProfile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        form = VisitorProfileForm(
            request.POST,
            instance=profile,
        )

        if form.is_valid():
            form.save()
            return redirect("visits:plan")
    else:
        form = VisitorProfileForm(instance=profile)

    return render(
        request,
        "accounts/preferences.html",
        {"form": form},
    )
