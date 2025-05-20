from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect
from django.contrib.auth import login

import uuid

from .models import Reader

User = get_user_model()

from django.contrib.auth.forms import UserCreationForm
from django import forms

class RegisterForm(UserCreationForm):
    ROLE_CHOICES = (
        ("reader", "Reader"),
        ("staff", "Staff"),
    )
    role = forms.ChoiceField(choices=ROLE_CHOICES, widget=forms.RadioSelect)

    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + ("first_name", "last_name", "email")

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
            return redirect("users:librarian_dashboard")
    else:
        form = RegisterForm()

    return render(request, "users/register.html", {"form": form})
