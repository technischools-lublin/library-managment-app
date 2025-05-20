from django.contrib.auth.decorators import (
    login_required,
)
from django.shortcuts import (
    render,
    get_object_or_404,
    redirect,
)
from users.models import Loan
from users.views import staff_required

from .models import Book

@login_required
def books_list(request):
    books = Book.objects.all()
    return render(request, 'catalog/books_list.html', {'books': books})

@login_required
def book_details(request, pk):
    book = get_object_or_404(Book, pk=pk)
    return render(request, 'catalog/book_details.html', {'book': book})

@login_required
def loans(request):
    reader = getattr(request.user, 'reader', None)
    if not reader:
        return render(request, 'catalog/loans.html', {
            'title': 'Your Loans',
            'headers': [],
            'rows': []
        })

    loans = Loan.objects.filter(reader=reader).select_related('book', 'reader__user')

    headers = ['Book', 'Borrowed At', 'Due At', 'Returned At', 'Fine', 'Overdue']
    rows = []
    for loan in loans:
        rows.append([
            loan.book.title,
            loan.borrowed_at,
            loan.due_at,
            loan.returned_at or '',
            f"${loan.fine:.2f}",
            'Yes' if loan.is_overdue else 'No'
        ])

    return render(request, 'catalog/loans.html', {
        'title': 'Your Loans',
        'headers': headers,
        'rows': rows
    })