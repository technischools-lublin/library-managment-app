from django.contrib.auth.decorators import (
    login_required,
)
from django.shortcuts import (
    render,
    get_object_or_404
)


from .models import Book
@login_required
def books_list(request):
    books = Book.objects.all()
    return render(request, 'catalog/books_list.html', {'books': books})

@login_required
def book_details(request, pk):
    book = get_object_or_404(Book, pk=pk)
    return render(request, 'catalog/book_details.html', {'book': book})

