from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

User = get_user_model()

class RegisterForm(UserCreationForm):
    ROLE_CHOICES = (("reader", "Reader"), ("staff", "Librarian"))
    role = forms.ChoiceField(choices=ROLE_CHOICES, widget=forms.RadioSelect)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = (
            "username",
            "role",
            "password1",
            "password2",
        )
