from django.db import models


class Book(models.Model):
    title = models.TextField()
    author = models.TextField()
    isbn = models.TextField()

    @property
    def is_available(self) -> bool:
        return not self.loans.filter(returned_at__isnull=True).exists()

    def __str__(self):
        return self.title


