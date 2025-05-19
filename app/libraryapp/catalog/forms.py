import uuid

from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

from .models import Book, Loan, Reader

User = get_user_model()


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ("title", "author", "isbn")


class ReaderForm(forms.ModelForm):
    first_name = forms.CharField(max_length=150)
    last_name = forms.CharField(max_length=150)
    email = forms.EmailField()

    class Meta:
        model = Reader
        fields = ("card_number",)

    def save(self, commit=True):
        reader = super().save(commit=False)
        user, _ = User.objects.get_or_create(
            username=self.cleaned_data["email"],
            defaults=dict(
                first_name=self.cleaned_data["first_name"],
                last_name=self.cleaned_data["last_name"],
                email=self.cleaned_data["email"],
                password=User.objects.make_random_password(),
            ),
        )
        reader.user = user
        if not reader.card_number:
            reader.card_number = str(uuid.uuid4())[:8]
        if commit:
            user.save()
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
