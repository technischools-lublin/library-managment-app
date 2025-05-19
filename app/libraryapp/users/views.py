import uuid

from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import redirect, render

from catalog.models import Reader
from .forms import RegisterForm

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            role = form.cleaned_data["role"]

            user.is_staff = role == "staff"
            user.save()

            if not user.is_staff:
                Reader.objects.create(
                    user=user, card_number=str(uuid.uuid4())[:8]
                )

            login(request, user)
            return redirect("catalog:librarian_dashboard")
    else:
        form = RegisterForm()

    return render(request, "users/register.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect("catalog:librarian_dashboard")
    else:
        form = AuthenticationForm()
    return render(request, "users/login.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect("users:login")


@login_required
def home(request):
    return render(request, "users/home.html")
