# LMA - Library Management App

An internal web application for managing library operations, built with Python and Django.
The system supports librarians in day-to-day work and gives readers self-service access to their loans.

## Project goal

The main goal is to streamline library workflows:
- book catalog management,
- reader registration and management,
- borrowing and returning books,
- overdue loan tracking,
- automatic late fee calculation.

## Core features

### Librarian features (`is_staff`)
- add books to the catalog,
- add readers,
- create loans,
- view active loans,
- register book returns,
- view overdue loans.

### Reader features
- dashboard with active loans,
- history preview of recently returned loans,
- personal loan list with overdue and fee information.

### Business rules
- one book can have only one active loan at a time,
- the system blocks borrowing when a book is already on loan,
- overdue fee is calculated per day after the due date (`0.50` per day).

## Technology stack

- Python
- Django
- SQLite (default development database)
- Django Templates (server-side rendering)

## Project structure

- `app/libraryapp/catalog` - book catalog, list and detail views,
- `app/libraryapp/users` - users, readers, loans, forms,
- `app/libraryapp/libraryapp` - Django project configuration,
- `app/requirements.txt` - project dependencies.

## Local setup

1. Go to the application directory:
	`app/libraryapp`
2. Create and activate a virtual environment.
3. Install dependencies:
	`pip install -r ../requirements.txt`
4. Apply migrations:
	`python manage.py migrate`
5. (Optional) create an admin user:
	`python manage.py createsuperuser`
6. Start the development server:
	`python manage.py runserver`

Then open:
`http://127.0.0.1:8000/`

## Example routes

- `/login/` - login,
- `/register/` - registration,
- `/books/` - book list,
- `/loans/` - reader loan list,
- `/loans/active/` - active loans (librarian),
- `/loans/overdue/` - overdue loans (librarian),
- `/admin/` - Django admin panel.

## Domain model (current implementation)

- `Book` - book data (`title`, `author`, `isbn`),
- `Reader` - reader profile linked 1:1 to a user,
- `Loan` - borrowing record (`borrowed_at`, `due_at`, `returned_at`) with overdue and fee logic.

## Authors

- Tomasz Zając
- Patryk Jurak
