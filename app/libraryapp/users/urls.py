from django.urls import path
from . import views

app_name = "users"


urlpatterns = [
    path("", views.librarian_dashboard, name="librarian_dashboard"),
    path("reader/", views.reader_dashboard, name="reader_dashboard"),
    path("register/", views.register, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("home/", views.home, name="home"),
    path("readers/add/", views.reader_add, name="reader_add"),
    path("books/add/", views.book_add, name="book_add"),

    path("readers/", views.readers_list, name="readers_list"),
    path("readers/add/", views.reader_add, name="reader_add"),

    path("loans/add/", views.loan_add, name="loan_add"),
    path("loans/active/", views.loans_active, name="loans_active"),
    path("loans/<int:pk>/return/", views.loan_return, name="loan_return"),
    path("loans/overdue/", views.loans_overdue, name="loans_overdue"),
]
