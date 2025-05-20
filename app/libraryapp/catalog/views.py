from django.contrib.auth.decorators import (
    login_required,
    user_passes_test,
)
from django.shortcuts import (
    render,
    redirect,
    get_object_or_404,
)


from .models import Book
from .forms import BookForm


staff_required = user_passes_test(lambda u: u.is_staff)

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
            "is_available": book.is_available,
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

