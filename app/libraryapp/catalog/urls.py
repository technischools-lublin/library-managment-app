from django.urls import path
from . import views

app_name = "catalog"

urlpatterns = [
    path('books/', views.books_list, name='books_list'),
    path("books/<int:pk>/", views.book_details, name="book_details"),
    path("loans/", views.loans, name="loans"),
]
