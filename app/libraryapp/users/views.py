import uuid

from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib import messages

from .forms import RegisterForm

from datetime import date
from decimal import Decimal

from .models import Reader, Loan
from catalog.forms import ReaderForm, LoanForm


staff_required = user_passes_test(lambda u: u.is_staff)

@login_required
def reader_dashboard(request):
    reader = request.user.reader
    if reader is None:
        return render(request, "users/reader_dashboard.html", {"error": "Nie jesteś czytelnikiem."})

    active_loans = reader.loans.filter(returned_at__isnull=True).select_related("book")
    past_loans = reader.loans.filter(returned_at__isnull=False).select_related("book").order_by("-returned_at")[:5]

    return render(
        request,
        "users/reader_dashboard.html",
        {
            "reader": reader,
            "active_loans": active_loans,
            "past_loans": past_loans,
        },
    )

@login_required
@staff_required
def librarian_dashboard(request):
    return render(request, "users/librarian_dashboard.html")


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


def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if getattr(user, "reader", None):
                return redirect("users:reader_dashboard")
            elif user.is_staff:
                return redirect("users:librarian_dashboard")
            else:
                return redirect("users:home")
    else:
        form = AuthenticationForm()
    return render(request, "users/login.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect("users:login")


@login_required
def home(request):
    return render(request, "users/home.html")

@login_required
@staff_required
def readers_list(request):
    readers = Reader.objects.select_related("user")
    return render(request, "users/readers_list.html", {"readers": readers})


@login_required
@staff_required
def reader_add(request):
    if request.method == "POST":
        form = ReaderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("users:readers_list")
    else:
        form = ReaderForm()
    return render(request, "users/reader_form.html", {"form": form})



@login_required
@staff_required
def loan_add(request):
    if request.method == "POST":
        form = LoanForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("users:loans_active")
    else:
        form = LoanForm()
    return render(request, "users/loan_form.html", {"form": form})


@login_required
@staff_required
def loans_active(request):
    loans = Loan.objects.filter(returned_at__isnull=True).select_related("book", "reader")
    return render(request, "users/loans_active.html", {"loans": loans})


@login_required
@staff_required
def loan_return(request, pk):
    loan = get_object_or_404(Loan, pk=pk, returned_at__isnull=True)
    loan.returned_at = date.today()
    loan.save()

    fine = loan.fine
    if fine > Decimal("0.00"):
        messages.warning(request, f"Overdue fine: {fine} PLN")
    else:
        messages.success(request, "Book returned without fine.")
    return redirect("users:loans_active")


@login_required
@staff_required
def loans_overdue(request):
    overdue = Loan.objects.filter(returned_at__isnull=True, due_at__lt=date.today()).select_related(
        "book", "reader"
    )
    return render(request, "users/loans_overdue.html", {"loans": overdue})