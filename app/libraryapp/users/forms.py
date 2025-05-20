from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from catalog.models import Book
from .models import Reader, Loan
import uuid

User = get_user_model()

class RegisterForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + ("first_name", "last_name", "email")

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
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

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ("title", "author", "isbn")


class ReaderForm(forms.ModelForm):
    username = forms.CharField(max_length=150)
    password1 = forms.CharField(widget=forms.PasswordInput, required=False)
    first_name = forms.CharField(max_length=150)
    last_name = forms.CharField(max_length=150)
    email = forms.EmailField()

    class Meta:
        model = Reader
        fields = ("card_number", "username", "password1", "first_name", "last_name", "email")

    def save(self, commit=True):
        User = get_user_model()
        username = self.cleaned_data["username"]
        password = self.cleaned_data.get("password1") or "admin1234"
        first_name = self.cleaned_data["first_name"]
        last_name = self.cleaned_data["last_name"]
        email = self.cleaned_data["email"]
        user = User.objects.create_user(
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
            email=email
        )
        reader = Reader(
            user=user,
            card_number=self.cleaned_data["card_number"] or f"CARD{user.id:05d}"
        )
        if commit:
            reader.save()
        return reader

class LoanForm(forms.ModelForm):
    class Meta:
        model = Loan
        fields = ("book", "reader", "due_at")
        widgets = {"due_at": forms.DateInput(attrs={"type": "date"})}

    def clean_book(self):
        book = self.cleaned_data["book"]
        if not book.is_available:
            raise ValidationError("This book is currently on loan.")
        return book
