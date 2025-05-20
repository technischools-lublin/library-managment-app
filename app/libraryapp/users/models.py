from django.db import models

from django.db import models
from django.contrib.auth import get_user_model

from datetime import date
from decimal import Decimal

from django.core.exceptions import ValidationError
from catalog.models import Book

User = get_user_model()

class Reader(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    card_number = models.CharField(max_length=16, unique=True)

    def __str__(self):
        return f"{self.user.username} ({self.card_number})"

class Loan(models.Model):
    book = models.ForeignKey(Book, related_name='loans', on_delete=models.PROTECT)
    reader = models.ForeignKey(Reader, related_name='loans', on_delete=models.PROTECT)
    borrowed_at = models.DateField(auto_now_add=True)
    due_at = models.DateField()
    returned_at = models.DateField(null=True, blank=True)

    DAILY_FINE = Decimal('0.50')

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['book'],
                condition=models.Q(returned_at__isnull=True),
                name='book_must_be_unique_when_on_loan'
            )
        ]

    def __str__(self):
        return f'{self.book}: {self.reader}'

    def clean(self):
        if not self.pk and getattr(self, 'book', None) and self.book and not self.book.is_available:
            raise ValidationError("This book is currently on loan.")

    @property
    def fine(self) -> Decimal:
        if self.returned_at and self.returned_at > self.due_at:
            days = (self.returned_at - self.due_at).days
            return days * self.DAILY_FINE
        return Decimal('0.00')

    @property
    def is_overdue(self) -> bool:
        return self.returned_at is None and date.today() > self.due_at

def get_reader(self):
    try:
        return Reader.objects.get(user=self)
    except Reader.DoesNotExist:
        return None

User.add_to_class("reader", property(get_reader))