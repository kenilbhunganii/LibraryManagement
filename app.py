from flask import Flask, render_template, request, redirect, url_for, flash
import json
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = "libris-secret-key-2024"

DATA_DIR = "data"
BOOKS_FILE = os.path.join(DATA_DIR, "books.json")
USERS_FILE = os.path.join(DATA_DIR, "users.json")
ACTIVITY_FILE = os.path.join(DATA_DIR, "activity.json")


# ── DATA HELPERS ──────────────────────────────────────────────────────────────

def load_books():
    try:
        with open(BOOKS_FILE, "r") as f:
            return json.load(f)
    except Exception:
        return []


def save_books(books):
    with open(BOOKS_FILE, "w") as f:
        json.dump(books, f, indent=4)


def load_users():
    try:
        with open(USERS_FILE, "r") as f:
            return json.load(f)
    except Exception:
        return []


def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=4)


def load_activity():
    try:
        with open(ACTIVITY_FILE, "r") as f:
            return json.load(f)
    except Exception:
        return []


def save_activity(activity):
    with open(ACTIVITY_FILE, "w") as f:
        json.dump(activity, f, indent=4)


def log_activity(entry_type, user_name, book_title):
    activity = load_activity()
    activity.insert(0, {
        "type": entry_type,
        "user": user_name,
        "book": book_title,
        "date": datetime.now().strftime("%d %b %Y")
    })
    save_activity(activity[:100])  # keep last 100


# ── ROUTES ────────────────────────────────────────────────────────────────────

@app.route("/")
def home():
    books = load_books()
    users = load_users()
    activity = load_activity()

    total_books     = len(books)
    available_books = sum(1 for b in books if b.get("available", True))
    borrowed_books  = total_books - available_books
    total_users     = len(users)
    recent_books    = books[-5:][::-1]
    recent_activity = activity[:6]

    return render_template("index.html",
        total_books=total_books,
        available_books=available_books,
        borrowed_books=borrowed_books,
        total_users=total_users,
        recent_books=recent_books,
        recent_activity=recent_activity
    )


# ── BOOKS ─────────────────────────────────────────────────────────────────────

@app.route("/books")
def books():
    return render_template("books.html", books=load_books())


@app.route("/books/add", methods=["GET", "POST"])
def add_book():
    if request.method == "POST":
        title       = request.form["title"].strip()
        author      = request.form["author"].strip()
        year        = request.form["year"].strip()
        isbn        = request.form["isbn"].strip()
        genre       = request.form.get("genre", "").strip()
        description = request.form.get("description", "").strip()

        books = load_books()

        if any(b["isbn"] == isbn for b in books):
            flash("A book with this ISBN already exists.", "error")
            return redirect(url_for("add_book"))

        books.append({
            "title":       title,
            "author":      author,
            "year":        year,
            "isbn":        isbn,
            "genre":       genre,
            "description": description,
            "available":   True,
            "borrowed_by": None
        })
        save_books(books)
        log_activity("add", "System", title)
        flash(f'Book "{title}" added successfully.', "success")
        return redirect(url_for("books"))

    return render_template("add_book.html")


@app.route("/books/<isbn>")
def book_detail(isbn):
    books = load_books()
    book  = next((b for b in books if b["isbn"] == isbn), None)

    if not book:
        flash("Book not found.", "error")
        return redirect(url_for("books"))

    activity     = load_activity()
    book_history = [e for e in activity if e.get("book") == book["title"]]

    return render_template("book_detail.html", book=book, book_history=book_history[:10])


@app.route("/books/delete/<isbn>", methods=["POST"])
def delete_book_route(isbn):
    books = load_books()
    book  = next((b for b in books if b["isbn"] == isbn), None)

    if book:
        books = [b for b in books if b["isbn"] != isbn]
        save_books(books)
        flash(f'Book "{book["title"]}" deleted.', "success")
    else:
        flash("Book not found.", "error")

    return redirect(url_for("books"))


# ── USERS ─────────────────────────────────────────────────────────────────────

@app.route("/users")
def users():
    return render_template("users.html", users=load_users())


@app.route("/users/add", methods=["GET", "POST"])
def add_user():
    if request.method == "POST":
        name    = request.form["name"].strip()
        user_id = request.form["user_id"].strip()
        email   = request.form.get("email", "").strip()
        phone   = request.form.get("phone", "").strip()

        users_list = load_users()

        if any(u["user_id"] == user_id for u in users_list):
            flash("A member with this ID already exists.", "error")
            return redirect(url_for("add_user"))

        users_list.append({
            "name":           name,
            "user_id":        user_id,
            "email":          email,
            "phone":          phone,
            "borrowed_books": []
        })
        save_users(users_list)
        flash(f'Member "{name}" registered.', "success")
        return redirect(url_for("users"))

    # ← Only this line changed: pass existing_ids
    users_list = load_users()
    existing_ids = [u["user_id"] for u in users_list]
    return render_template("add_user.html", existing_ids=existing_ids)


@app.route("/users/delete/<user_id>", methods=["POST"])
def delete_user_route(user_id):
    users_list = load_users()
    user       = next((u for u in users_list if u["user_id"] == user_id), None)

    if user:
        users_list = [u for u in users_list if u["user_id"] != user_id]
        save_users(users_list)
        flash(f'Member "{user["name"]}" removed.', "success")
    else:
        flash("Member not found.", "error")

    return redirect(url_for("users"))


# ── BORROW / RETURN ───────────────────────────────────────────────────────────

@app.route("/borrow", methods=["GET", "POST"])
def borrow():
    books_list = load_books()
    users_list = load_users()

    available_books = [b for b in books_list if b.get("available", True)]
    borrowed_books  = [b for b in books_list if not b.get("available", True)]

    if request.method == "POST":
        action  = request.form.get("action")
        isbn    = request.form.get("isbn", "").strip()
        user_id = request.form.get("user_id", "").strip()

        book = next((b for b in books_list if b["isbn"] == isbn), None)
        user = next((u for u in users_list if u["user_id"] == user_id), None)

        if not book:
            flash("Book not found.", "error")
            return redirect(url_for("borrow"))
        if not user:
            flash("Member not found.", "error")
            return redirect(url_for("borrow"))

        if action == "borrow":
            if not book.get("available", True):
                flash("This book is already borrowed.", "error")
            else:
                book["available"]  = False
                book["borrowed_by"] = user["name"]
                if isbn not in user["borrowed_books"]:
                    user["borrowed_books"].append(isbn)
                save_books(books_list)
                save_users(users_list)
                log_activity("borrow", user["name"], book["title"])
                flash(f'"{book["title"]}" issued to {user["name"]}.', "success")

        elif action == "return":
            if book.get("available", True):
                flash("This book is already marked as available.", "error")
            else:
                book["available"]  = True
                book["borrowed_by"] = None
                if isbn in user["borrowed_books"]:
                    user["borrowed_books"].remove(isbn)
                save_books(books_list)
                save_users(users_list)
                log_activity("return", user["name"], book["title"])
                flash(f'"{book["title"]}" returned by {user["name"]}.', "success")

        return redirect(url_for("borrow"))

    return render_template("borrow.html",
        available_books=available_books,
        borrowed_books=borrowed_books,
        users=users_list
    )


# ── SEARCH ────────────────────────────────────────────────────────────────────

@app.route("/search")
def search():
    query      = request.args.get("q", "").strip()
    books_list = load_books()
    results    = []

    if query:
        q = query.lower()
        results = [
            b for b in books_list
            if q in b.get("title",  "").lower()
            or q in b.get("author", "").lower()
            or q in b.get("isbn",   "").lower()
            or q in b.get("genre",  "").lower()
        ]

    return render_template("search.html",
        query=query,
        results=results,
        all_books=books_list
    )


# ── ACTIVITY ──────────────────────────────────────────────────────────────────

@app.route("/activity")
def activity():
    return render_template("activity.html", activity=load_activity())


# ── STATS ─────────────────────────────────────────────────────────────────────

@app.route("/stats")
def stats():
    books_list    = load_books()
    users_list    = load_users()
    activity_list = load_activity()

    total_books     = len(books_list)
    available_books = sum(1 for b in books_list if b.get("available", True))
    borrowed_books  = total_books - available_books
    total_users     = len(users_list)

    # Genre breakdown
    genre_stats = {}
    for b in books_list:
        g = b.get("genre") or "Unknown"
        genre_stats[g] = genre_stats.get(g, 0) + 1
    genre_stats = dict(sorted(genre_stats.items(), key=lambda x: -x[1]))

    # Top borrowers from activity log
    borrow_counts = {}
    for entry in activity_list:
        if entry.get("type") == "borrow":
            name = entry.get("user", "Unknown")
            borrow_counts[name] = borrow_counts.get(name, 0) + 1

    top_members = sorted(
        [{"name": k, "count": v} for k, v in borrow_counts.items()],
        key=lambda x: -x["count"]
    )[:5]

    return render_template("stats.html",
        total_books=total_books,
        available_books=available_books,
        borrowed_books=borrowed_books,
        total_users=total_users,
        genre_stats=genre_stats,
        top_members=top_members
    )


# ── MAIN ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    os.makedirs(DATA_DIR, exist_ok=True)
    for f in [BOOKS_FILE, USERS_FILE, ACTIVITY_FILE]:
        if not os.path.exists(f):
            with open(f, "w") as fh:
                json.dump([], fh)
    app.run(debug=True)