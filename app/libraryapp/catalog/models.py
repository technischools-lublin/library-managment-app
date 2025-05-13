from django.db import models

# Create your models here.

class Book(models.Model):
    title = models.TextField()
    author = models.TextField()
    isbn = models.TextField()

    def __str__(self):
        return self.title