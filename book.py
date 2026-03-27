class Book:
    def __init__(self, title, author, year, isbn, genre="", description=""):
        self.title = title
        self.author = author
        self.year = year
        self.isbn = isbn
        self.genre = genre
        self.description = description
        self.available = True
        self.borrowed_by = None

    def borrow(self, user_name=None):
        self.available = False
        self.borrowed_by = user_name

    def return_book(self):
        self.available = True
        self.borrowed_by = None

    def to_dict(self):
        return {
            "title": self.title,
            "author": self.author,
            "year": self.year,
            "isbn": self.isbn,
            "genre": self.genre,
            "description": self.description,
            "available": self.available,
            "borrowed_by": self.borrowed_by
        }

    def __str__(self):
        status = "Available" if self.available else f"Borrowed by {self.borrowed_by}"
        return f"{self.title} by {self.author} ({self.year}) — {status}"

    def __repr__(self):
        return f"Book(title={self.title!r}, isbn={self.isbn!r})"