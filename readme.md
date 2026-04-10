# Libris — Library Management System

A lightweight, web-based library management system built with **Python 3.10** and **Flask**. Libris lets you manage books and members, handle borrowing and returning, search the catalogue, and view activity logs and statistics — all from a clean browser interface.

---

## Complete Project Structure

```
library-management/
│
├── app.py                        # Flask application — all routes and business logic
├── book.py                       # Book class definition
├── library.py                    # Helper/utility functions (search, stats, etc.)
├── user.py                       # User (Member) class definition
│
├── data/                         # JSON-based persistent storage
│   ├── activity.json             # Activity log (last 100 events)
│   ├── books.json                # Book records
│   └── users.json                # Member records
│
├── static/                       # Frontend static assets
│   ├── script.js                 # Client-side JavaScript (3 KB)
│   └── style.css                 # Global stylesheet (26 KB)
│
├── templates/                    # Jinja2 HTML templates
│   ├── base.html                 # Base layout (navigation, header, footer)
│   ├── index.html                # Dashboard / home page
│   ├── books.html                # Book listing page
│   ├── add_book.html             # Add new book form
│   ├── book_detail.html          # Individual book detail page
│   ├── users.html                # Member listing page
│   ├── add_user.html             # Register new member form
│   ├── borrow.html               # Borrow / return page
│   ├── search.html               # Search results page
│   ├── activity.html             # Activity log page
│   └── stats.html                # Statistics & analytics page
│
├── .trunk/                       # Trunk.io code quality tooling
│   ├── actions/                  # Custom trunk actions
│   ├── configs/                  # Linter/formatter configurations
│   ├── logs/                     # Trunk execution logs
│   ├── notifications/            # Trunk notifications
│   ├── out/                      # Trunk output files
│   ├── plugins/                  # Trunk plugins
│   ├── tools/                    # Trunk managed tools
│   ├── .gitignore                # Trunk-specific gitignore rules
│   └── trunk.yaml                # Main Trunk configuration file
│
└── __pycache__/                  # Python bytecode cache (auto-generated, do not edit)
    ├── book.cpython-310.pyc
    ├── email_utils.cpython-310.pyc
    ├── library.cpython-310.pyc
    └── user.cpython-310.pyc
```

---

## Features

- **Dashboard** — Overview of total books, available/borrowed counts, recent additions, and recent activity
- **Book Management** — Add, view, and delete books with title, author, year, ISBN, genre, and description
- **Member Management** — Register and remove library members with name, ID, email, and phone
- **Borrow & Return** — Issue books to members and process returns with a single form
- **Search** — Full-text search across title, author, ISBN, and genre (partial matches supported)
- **Activity Log** — Full history of borrows, returns, and additions (last 100 events stored)
- **Statistics** — Genre breakdown and top borrowers leaderboard

---

## Getting Started

### Prerequisites

- Python 3.10+
- pip

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/library-management.git
   cd library-management
   ```

2. **Install dependencies**
   ```bash
   pip install flask
   ```

3. **Run the application**
   ```bash
   python app.py
   ```

4. **Open in your browser**
   ```
   http://127.0.0.1:5000
   ```

> The `data/` directory and all JSON files (`books.json`, `users.json`, `activity.json`) are created automatically on first run if they don't exist.

---

## Usage Guide

### Adding a Book
1. Navigate to **Books → Add Book**
2. Fill in the title, author, year, and ISBN (required), plus optional genre and description
3. Click **Add Book** — the book is immediately available for borrowing

### Registering a Member
1. Navigate to **Members → Add Member**
2. Enter the member's name and a unique Member ID, plus optional email and phone
3. Click **Register** — the member can now borrow books

### Borrowing a Book
1. Navigate to **Borrow / Return**
2. Select an available book from the list and enter the Member ID
3. Click **Issue Book** — the book is marked as borrowed and linked to the member

### Returning a Book
1. Navigate to **Borrow / Return**
2. Select the borrowed book and enter the Member ID of the borrower
3. Click **Return Book** — the book is marked as available again

### Searching the Catalogue
- Use the **Search** page to find books by title, author, ISBN, or genre
- Partial and case-insensitive matches are supported

---

## Module Overview

### `book.py` — `Book` Class

Represents a single book in the library.

| Method | Description |
|---|---|
| `__init__(title, author, year, isbn, genre, description)` | Create a new book instance |
| `borrow(user_name)` | Mark book as borrowed, store borrower's name |
| `return_book()` | Mark book as available, clear borrower |
| `to_dict()` | Serialize to dictionary for JSON storage |
| `__str__()` | Human-readable string with availability status |
| `__repr__()` | Developer-friendly representation |

---

### `user.py` — `User` Class

Represents a library member.

| Method | Description |
|---|---|
| `__init__(name, user_id, email, phone)` | Create a new member instance |
| `borrow_book(isbn)` | Add ISBN to member's borrowed list |
| `return_book(isbn)` | Remove ISBN from member's borrowed list |
| `to_dict()` | Serialize to dictionary for JSON storage |
| `__str__()` | Human-readable string with borrow count |
| `__repr__()` | Developer-friendly representation |

---

### `library.py` — Helper Functions

Utility functions that operate on the in-memory book/user lists.

| Function | Description |
|---|---|
| `search_by_title(library, title)` | Partial, case-insensitive title search |
| `search_by_author(library, author)` | Partial, case-insensitive author search |
| `search_by_isbn(library, isbn)` | Exact ISBN lookup, returns single book or `None` |
| `delete_book(library, isbn)` | Remove a book by ISBN, returns `True`/`False` |
| `get_available_books(library)` | Return all books where `available == True` |
| `get_borrowed_books(library)` | Return all books where `available == False` |
| `get_stats(library, users)` | Return summary dict (total, available, borrowed, utilization %) |

---

### `app.py` — Flask Routes

| Route | Method(s) | Template | Description |
|---|---|---|---|
| `/` | GET | `index.html` | Dashboard with stats and recent activity |
| `/books` | GET | `books.html` | Full book catalogue list |
| `/books/add` | GET, POST | `add_book.html` | Add a new book form |
| `/books/<isbn>` | GET | `book_detail.html` | Individual book detail and borrow history |
| `/books/delete/<isbn>` | POST | — | Delete a book by ISBN |
| `/users` | GET | `users.html` | Full member list |
| `/users/add` | GET, POST | `add_user.html` | Register a new member form |
| `/users/delete/<user_id>` | POST | — | Remove a member by ID |
| `/borrow` | GET, POST | `borrow.html` | Borrow or return a book |
| `/search` | GET | `search.html` | Search catalogue by query string |
| `/activity` | GET | `activity.html` | Full activity log |
| `/stats` | GET | `stats.html` | Genre breakdown and top borrowers |

---

## Frontend

### `static/style.css` (26 KB)
Global stylesheet covering all pages — layout, navigation, cards, tables, forms, flash messages, and responsive design.

### `static/script.js` (3 KB)
Client-side JavaScript for interactive elements such as dynamic dropdowns, form validation, and flash message dismissal.

### `templates/base.html`
The base Jinja2 layout that all other templates extend. Contains the navigation bar, page wrapper, flash message display area, and footer. All child templates use `{% extends "base.html" %}`.

---

## Data Storage

All data is stored as plain JSON files in the `data/` directory — no database setup required.

### `data/books.json`
```json
[
  {
    "title": "The Great Gatsby",
    "author": "F. Scott Fitzgerald",
    "year": "1925",
    "isbn": "9780743273565",
    "genre": "Fiction",
    "description": "A story of wealth and ambition.",
    "available": true,
    "borrowed_by": null
  }
]
```

### `data/users.json`
```json
[
  {
    "name": "Alice Johnson",
    "user_id": "U001",
    "email": "alice@example.com",
    "phone": "9876543210",
    "borrowed_books": []
  }
]
```

### `data/activity.json`
```json
[
  {
    "type": "borrow",
    "user": "Alice Johnson",
    "book": "The Great Gatsby",
    "date": "10 Apr 2026"
  }
]
```
> Activity log is automatically capped at **100 entries** (oldest entries are dropped automatically).

---

## Tech Stack

| Layer | Technology |
|---|---|
| Language | Python 3.10 |
| Web Framework | Flask |
| Templating | Jinja2 |
| Frontend | HTML5, CSS3, JavaScript |
| Storage | JSON flat files |
| Code Quality | Trunk.io |

---

## Code Quality — Trunk

This project uses **[Trunk](https://trunk.io/)** for automated linting, formatting, and code quality enforcement. The `.trunk/` directory contains all Trunk configuration.

| File / Folder | Purpose |
|---|---|
| `trunk.yaml` | Main config — enabled linters, formatters, and tools |
| `.gitignore` | Trunk-specific gitignore rules |
| `configs/` | Per-linter config files |
| `plugins/` | Trunk plugin definitions |
| `actions/` | Custom Trunk CI actions |
| `tools/` | Trunk-managed tool binaries |
| `logs/` | Trunk execution logs |
| `out/` | Output artifacts from Trunk runs |
| `notifications/` | Trunk notification settings |

**Run Trunk locally:**
```bash
# Check for issues
trunk check

# Auto-format code
trunk fmt
```

---

## Potential Improvements

- Add due dates and overdue tracking with email reminders (`email_utils.py` already present in codebase)
- User authentication and admin/librarian roles
- SQLite or PostgreSQL backend for larger collections
- REST API for mobile or third-party integrations
- Export reports to CSV or PDF
- Book cover image upload support
- Barcode/QR code scanning for ISBN input

---

## License

This project is open source. Feel free to use, modify, and distribute it.

---

## Author

Developed by **Kenil Bhungani**