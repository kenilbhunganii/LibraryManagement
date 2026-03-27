def search_by_title(library, title):
    """Search books by title (partial match, case-insensitive)."""
    q = title.lower()
    return [b for b in library if q in b.get("title", "").lower()]


def search_by_author(library, author):
    """Search books by author (partial match, case-insensitive)."""
    q = author.lower()
    return [b for b in library if q in b.get("author", "").lower()]


def search_by_isbn(library, isbn):
    """Find a book by exact ISBN."""
    return next((b for b in library if b.get("isbn") == isbn), None)


def delete_book(library, isbn):
    """Remove a book by ISBN. Returns True if removed, False if not found."""
    for i, book in enumerate(library):
        if book.get("isbn") == isbn:
            library.pop(i)
            return True
    return False


def get_available_books(library):
    """Return all available (not borrowed) books."""
    return [b for b in library if b.get("available", True)]


def get_borrowed_books(library):
    """Return all borrowed books."""
    return [b for b in library if not b.get("available", True)]


def get_stats(library, users):
    """Return a summary dictionary of library statistics."""
    total = len(library)
    available = sum(1 for b in library if b.get("available", True))
    return {
        "total_books": total,
        "available": available,
        "borrowed": total - available,
        "total_users": len(users),
        "utilization_pct": round((total - available) / total * 100) if total else 0
    }