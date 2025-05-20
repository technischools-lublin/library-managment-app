from django.contrib.auth.decorators import (
    login_required,
)
from django.shortcuts import (
    render,
    get_object_or_404
)
from users.models import Loan

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
    loans = Loan.objects.select_related('book', 'reader__user').all()

    headers = ['Book', 'Reader', 'Borrowed At', 'Due At', 'Returned At', 'Fine', 'Overdue']
    rows = []
    for loan in loans:
        rows.append([
            loan.book.title,
            loan.reader.user.get_full_name(),
            loan.borrowed_at,
            loan.due_at,
            loan.returned_at or '',
            f"${loan.fine:.2f}",
            'Yes' if loan.is_overdue else 'No'
        ])

    return render(request, 'catalog/loans.html', {
        'title': 'All Loans',
        'headers': headers,
        'rows': rows
    })