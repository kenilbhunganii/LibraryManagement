class User:
    def __init__(self, name, user_id, email="", phone=""):
        self.name = name
        self.user_id = user_id
        self.email = email
        self.phone = phone
        self.borrowed_books = []  # list of ISBNs

    def borrow_book(self, isbn):
        if isbn not in self.borrowed_books:
            self.borrowed_books.append(isbn)

    def return_book(self, isbn):
        if isbn in self.borrowed_books:
            self.borrowed_books.remove(isbn)

    def to_dict(self):
        return {
            "name": self.name,
            "user_id": self.user_id,
            "email": self.email,
            "phone": self.phone,
            "borrowed_books": self.borrowed_books
        }

    def __str__(self):
        return f"Member: {self.name} (ID: {self.user_id}) — {len(self.borrowed_books)} book(s) borrowed"

    def __repr__(self):
        return f"User(name={self.name!r}, user_id={self.user_id!r})"