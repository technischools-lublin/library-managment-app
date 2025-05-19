from datetime import date
from decimal import Decimal

from django.contrib import messages
from django.contrib.auth.decorators import (
    login_required,
    user_passes_test,
)
from django.shortcuts import (
    render,
    redirect,
    get_object_or_404,
)

from .models import Book, Reader, Loan
from .forms import BookForm, ReaderForm, LoanForm   # you’ll create these


staff_required = user_passes_test(lambda u: u.is_staff)

@login_required
@staff_required
def librarian_dashboard(request):
    return render(request, "catalog/librarian_dashboard.html")

@login_required
@staff_required
def book_add(request):
    if request.method == "POST":
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("catalog:books_list")
    else:
        form = BookForm()
    return render(request, "catalog/book_form.html", {"form": form})

@login_required
def books_list(request):
    books = Book.objects.all()
    return render(request, 'catalog/books_list.html', {'books': books})

@login_required
@staff_required
def book_details(request, pk):
    book = get_object_or_404(Book, pk=pk)
    loans = (
        book.loans.select_related("reader", "reader__user")
        .order_by("-borrowed_at")
    )
    return render(
        request,
        "catalog/book_details.html",
        {
            "book": book,
            "is_available": book.isAvailable,
            "loans": loans,
        },
    )

@login_required
@staff_required
def book_edit(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == "POST":
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect("catalog:books_list")
    else:
        form = BookForm(instance=book)
    return render(request, "catalog/book_form.html", {"form": form})


@login_required
@staff_required
def readers_list(request):
    readers = Reader.objects.select_related("user")
    return render(request, "catalog/readers_list.html", {"readers": readers})


@login_required
@staff_required
def reader_add(request):
    if request.method == "POST":
        form = ReaderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("catalog:readers_list")
    else:
        form = ReaderForm()
    return render(request, "catalog/reader_form.html", {"form": form})



@login_required
@staff_required
def loan_add(request):
    if request.method == "POST":
        form = LoanForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("catalog:loans_active")
    else:
        form = LoanForm()
    return render(request, "catalog/loan_form.html", {"form": form})


@login_required
@staff_required
def loans_active(request):
    loans = Loan.objects.filter(returned_at__isnull=True).select_related("book", "reader")
    return render(request, "catalog/loans_active.html", {"loans": loans})


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
    return redirect("catalog:loans_active")


@login_required
@staff_required
def loans_overdue(request):
    overdue = Loan.objects.filter(returned_at__isnull=True, due_at__lt=date.today()).select_related(
        "book", "reader"
    )
    return render(request, "catalog/loans_overdue.html", {"loans": overdue})
