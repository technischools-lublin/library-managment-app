from django.urls import path
from . import views

app_name = "catalog"

urlpatterns = [
    path('books/', views.books_list, name='books_list'),
    path("books/<int:pk>/", views.book_details, name="book_details"),
    path("books/add/", views.book_add, name="book_add"),
    path("books/<int:pk>/edit/", views.book_edit, name="book_edit"),

    path("readers/", views.readers_list, name="readers_list"),
    path("readers/add/", views.reader_add, name="reader_add"),

    path("loans/add/", views.loan_add, name="loan_add"),
    path("loans/active/", views.loans_active, name="loans_active"),
    path("loans/<int:pk>/return/", views.loan_return, name="loan_return"),
    path("loans/overdue/", views.loans_overdue, name="loans_overdue"),
]
