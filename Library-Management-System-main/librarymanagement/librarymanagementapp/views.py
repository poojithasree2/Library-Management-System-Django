from django.shortcuts import render, redirect
from datetime import datetime, timedelta
from decimal import Decimal
import pymysql


# =========================================================
# DATABASE CONNECTION
# =========================================================

def get_connection():

    return pymysql.connect(
        host="127.0.0.1",
        user="root",
        password="root",
        database="student",
        cursorclass=pymysql.cursors.Cursor
    )


# =========================================================
# SETTINGS
# =========================================================

FINE_PER_DAY = Decimal("10.00")

BOOKING_DAYS = 7


# =========================================================
# SESSION PROTECTION
# =========================================================

def student_required(request):

    return bool(
        request.session.get("student_id")
        and request.session.get("user_type") == "student"
    )


def admin_required(request):

    return bool(
        request.session.get("admin_logged_in")
        and request.session.get("user_type") == "admin"
    )


# =========================================================
# HOME
# =========================================================

def index(request):

    return render(
        request,
        "index.html"
    )


# =========================================================
# STUDENT SIGNUP
# =========================================================

def signup(request):

    if request.method == "POST":

        username = request.POST.get(
            "t1",
            ""
        ).strip()

        password = request.POST.get(
            "t2",
            ""
        )

        contact = request.POST.get(
            "t3",
            ""
        ).strip()

        email = request.POST.get(
            "t4",
            ""
        ).strip()

        address = request.POST.get(
            "t5",
            ""
        ).strip()

        if not username or not password:

            return render(
                request,
                "signup.html",
                {
                    "msg":
                    "Username and password are required."
                }
            )

        con = None

        try:

            con = get_connection()
            cur = con.cursor()

            cur.execute(
                """
                SELECT id
                FROM users
                WHERE username=%s
                LIMIT 1
                """,
                (username,)
            )

            user = cur.fetchone()

            if user:

                return render(
                    request,
                    "signup.html",
                    {
                        "msg":
                        "Username already exists."
                    }
                )

            cur.execute(
                """
                INSERT INTO users
                (
                    username,
                    password,
                    contact,
                    email,
                    address
                )
                VALUES
                (%s,%s,%s,%s,%s)
                """,
                (
                    username,
                    password,
                    contact,
                    email,
                    address
                )
            )

            con.commit()

            return render(
                request,
                "signup.html",
                {
                    "msg":
                    "Registration Successful. You can now login."
                }
            )

        except Exception as e:

            if con:
                con.rollback()

            return render(
                request,
                "signup.html",
                {
                    "msg":
                    "Registration Error: " + str(e)
                }
            )

        finally:

            if con:
                con.close()

    return render(
        request,
        "signup.html"
    )


# =========================================================
# STUDENT LOGIN
# =========================================================

def login(request):

    if request.method == "POST":

        username = request.POST.get(
            "t1",
            ""
        ).strip()

        password = request.POST.get(
            "t2",
            ""
        )

        if not username or not password:

            return render(
                request,
                "login.html",
                {
                    "msg":
                    "Please enter username and password."
                }
            )

        con = None
        user = None

        try:

            con = get_connection()
            cur = con.cursor()

            cur.execute(
                """
                SELECT
                    id,
                    username,
                    password,
                    contact,
                    email,
                    address
                FROM users
                WHERE username=%s
                LIMIT 1
                """,
                (username,)
            )

            user = cur.fetchone()

        except Exception as e:

            print(
                "LOGIN DATABASE ERROR:",
                e
            )

            return render(
                request,
                "login.html",
                {
                    "msg":
                    "Database Error: " + str(e)
                }
            )

        finally:

            if con:
                con.close()

        if not user:

            return render(
                request,
                "login.html",
                {
                    "msg":
                    "Username does not exist."
                }
            )

        stored_password = str(user[2])
        entered_password = str(password)

        if stored_password != entered_password:

            return render(
                request,
                "login.html",
                {
                    "msg":
                    "Incorrect password."
                }
            )

        request.session.flush()

        request.session["student_id"] = user[0]

        request.session["student_username"] = user[1]

        request.session["user_type"] = "student"

        request.session.save()

        return redirect(
            "student_home"
        )

    return render(
        request,
        "login.html"
    )


# =========================================================
# STUDENT DASHBOARD
# =========================================================

def student_home(request):

    if not student_required(request):

        return redirect("login")

    student_id = request.session.get(
        "student_id"
    )

    username = request.session.get(
        "student_username"
    )

    con = None

    available_books = 0
    my_bookings = 0
    overdue_books = 0
    total_fine = Decimal("0.00")
    notifications = 0

    try:

        con = get_connection()
        cur = con.cursor()

        cur.execute(
            """
            SELECT COALESCE(
                SUM(total_books),0
            )
            FROM books
            WHERE total_books > 0
            """
        )

        available_books = cur.fetchone()[0]

        cur.execute(
            """
            SELECT COUNT(*)
            FROM bookings
            WHERE student_id=%s
            AND status NOT IN
            ('Returned','Cancelled')
            """,
            (student_id,)
        )

        my_bookings = cur.fetchone()[0]

        cur.execute(
            """
            SELECT COUNT(*)
            FROM bookings
            WHERE student_id=%s
            AND due_date < CURDATE()
            AND status NOT IN
            ('Returned','Cancelled')
            """,
            (student_id,)
        )

        overdue_books = cur.fetchone()[0]

        cur.execute(
            """
            SELECT COALESCE(
                SUM(fine),0
            )
            FROM bookings
            WHERE student_id=%s
            """,
            (student_id,)
        )

        total_fine = cur.fetchone()[0]

        cur.execute(
            """
            SELECT COUNT(*)
            FROM bookings
            WHERE student_id=%s
            AND status NOT IN
            ('Returned','Cancelled')
            AND due_date <= DATE_ADD(
                CURDATE(),
                INTERVAL 2 DAY
            )
            """,
            (student_id,)
        )

        notifications = cur.fetchone()[0]

    except Exception as e:

        print(
            "STUDENT HOME ERROR:",
            e
        )

    finally:

        if con:
            con.close()

    return render(
        request,
        "student_home.html",
        {
            "username": username,
            "available_books": available_books,
            "my_bookings": my_bookings,
            "overdue_books": overdue_books,
            "total_fine": total_fine,
            "notifications": notifications
        }
    )


# =========================================================
# ADMIN LOGIN
# =========================================================

def admin_login(request):

    if request.method == "POST":

        username = request.POST.get(
            "t1",
            ""
        ).strip()

        password = request.POST.get(
            "t2",
            ""
        )

        if (
            username == "libraryadmin"
            and
            password == "Lib@1234"
        ):

            request.session.flush()

            request.session[
                "admin_logged_in"
            ] = True

            request.session[
                "admin_username"
            ] = username

            request.session[
                "user_type"
            ] = "admin"

            request.session.save()

            return redirect(
                "admin_home"
            )

        return render(
            request,
            "admin_login.html",
            {
                "msg":
                "Invalid Admin Username or Password"
            }
        )

    return render(
        request,
        "admin_login.html"
    )


# =========================================================
# ADMIN HOME
# =========================================================

def admin_home(request):

    if not admin_required(request):

        return redirect("admin_login")

    con = None

    total_book_titles = 0
    available_books = 0
    total_students = 0
    total_bookings = 0
    overdue_books = 0
    total_fine = Decimal("0.00")

    try:

        con = get_connection()
        cur = con.cursor()

        cur.execute(
            "SELECT COUNT(*) FROM books"
        )

        total_book_titles = cur.fetchone()[0]

        cur.execute(
            """
            SELECT COALESCE(
                SUM(total_books),0
            )
            FROM books
            """
        )

        available_books = cur.fetchone()[0]

        cur.execute(
            "SELECT COUNT(*) FROM users"
        )

        total_students = cur.fetchone()[0]

        cur.execute(
            "SELECT COUNT(*) FROM bookings"
        )

        total_bookings = cur.fetchone()[0]

        cur.execute(
            """
            SELECT COUNT(*)
            FROM bookings
            WHERE due_date < CURDATE()
            AND status NOT IN
            ('Returned','Cancelled')
            """
        )

        overdue_books = cur.fetchone()[0]

        cur.execute(
            """
            SELECT COALESCE(
                SUM(fine),0
            )
            FROM bookings
            """
        )

        total_fine = cur.fetchone()[0]

    except Exception as e:

        print(
            "ADMIN HOME ERROR:",
            e
        )

    finally:

        if con:
            con.close()

    return render(
        request,
        "admin_home.html",
        {
            "total_book_titles":
                total_book_titles,

            "available_books":
                available_books,

            "total_students":
                total_students,

            "total_bookings":
                total_bookings,

            "overdue_books":
                overdue_books,

            "total_fine":
                total_fine
        }
    )


# =========================================================
# ADMIN STATISTICS
# =========================================================

def admin_statistics(request):

    if not admin_required(request):

        return redirect("admin_login")

    con = None

    total_book_titles = 0
    total_books = 0
    total_students = 0
    total_bookings = 0
    active_bookings = 0
    returned_books = 0
    cancelled_bookings = 0
    overdue_books = 0
    total_fine = Decimal("0.00")

    try:

        con = get_connection()
        cur = con.cursor()

        cur.execute(
            "SELECT COUNT(*) FROM books"
        )

        total_book_titles = cur.fetchone()[0]

        cur.execute(
            """
            SELECT COALESCE(
                SUM(total_books),0
            )
            FROM books
            """
        )

        total_books = cur.fetchone()[0]

        cur.execute(
            "SELECT COUNT(*) FROM users"
        )

        total_students = cur.fetchone()[0]

        cur.execute(
            "SELECT COUNT(*) FROM bookings"
        )

        total_bookings = cur.fetchone()[0]

        cur.execute(
            """
            SELECT COUNT(*)
            FROM bookings
            WHERE status='Booked'
            """
        )

        active_bookings = cur.fetchone()[0]

        cur.execute(
            """
            SELECT COUNT(*)
            FROM bookings
            WHERE status='Returned'
            """
        )

        returned_books = cur.fetchone()[0]

        cur.execute(
            """
            SELECT COUNT(*)
            FROM bookings
            WHERE status='Cancelled'
            """
        )

        cancelled_bookings = cur.fetchone()[0]

        cur.execute(
            """
            SELECT COUNT(*)
            FROM bookings
            WHERE due_date < CURDATE()
            AND status NOT IN
            ('Returned','Cancelled')
            """
        )

        overdue_books = cur.fetchone()[0]

        cur.execute(
            """
            SELECT COALESCE(
                SUM(fine),0
            )
            FROM bookings
            """
        )

        total_fine = cur.fetchone()[0]

    except Exception as e:

        print(
            "ADMIN STATISTICS ERROR:",
            e
        )

    finally:

        if con:
            con.close()

    return render(
        request,
        "admin_statistics.html",
        {
            "total_book_titles":
                total_book_titles,

            "total_books":
                total_books,

            "total_students":
                total_students,

            "total_bookings":
                total_bookings,

            "active_bookings":
                active_bookings,

            "returned_books":
                returned_books,

            "cancelled_bookings":
                cancelled_bookings,

            "overdue_books":
                overdue_books,

            "total_fine":
                total_fine
        }
    )


# =========================================================
# AVAILABLE BOOKS
# =========================================================

def available_books(request):

    if not student_required(request):

        return redirect("login")

    con = get_connection()
    cur = con.cursor()

    try:

        cur.execute(
            """
            SELECT
                id,
                book_name,
                author,
                total_books,
                category,
                description,
                book_cover,
                status
            FROM books
            WHERE total_books > 0
            ORDER BY book_name
            """
        )

        books = cur.fetchall()

    finally:

        con.close()

    return render(
        request,
        "available_books.html",
        {
            "books": books
        }
    )


# =========================================================
# BOOK CATEGORIES
# =========================================================

def book_categories(request):

    if not student_required(request):

        return redirect("login")

    con = get_connection()
    cur = con.cursor()

    try:

        cur.execute(
            """
            SELECT
                category,
                COUNT(*)
            FROM books
            WHERE category IS NOT NULL
            AND category != ''
            GROUP BY category
            ORDER BY category
            """
        )

        categories = cur.fetchall()

    finally:

        con.close()

    return render(
        request,
        "book_categories.html",
        {
            "categories": categories
        }
    )


# =========================================================
# BOOK CATEGORY
# =========================================================

def book_category(request, category):

    if not student_required(request):

        return redirect("login")

    con = get_connection()
    cur = con.cursor()

    try:

        cur.execute(
            """
            SELECT
                id,
                book_name,
                author,
                total_books,
                category,
                description,
                book_cover,
                status
            FROM books
            WHERE category=%s
            ORDER BY book_name
            """,
            (category,)
        )

        books = cur.fetchall()

    finally:

        con.close()

    return render(
        request,
        "book_category.html",
        {
            "books": books,
            "category": category
        }
    )


# =========================================================
# SEARCH BOOKS
# =========================================================

def search_books(request):

    if (
        not student_required(request)
        and
        not admin_required(request)
    ):

        return redirect("login")

    search = request.GET.get(
        "search",
        ""
    ).strip()

    con = get_connection()
    cur = con.cursor()

    try:

        if search:

            value = "%" + search + "%"

            cur.execute(
                """
                SELECT
                    id,
                    book_name,
                    author,
                    total_books,
                    category,
                    description,
                    book_cover,
                    status
                FROM books
                WHERE
                    book_name LIKE %s
                    OR author LIKE %s
                    OR category LIKE %s
                ORDER BY book_name
                """,
                (
                    value,
                    value,
                    value
                )
            )

        else:

            cur.execute(
                """
                SELECT
                    id,
                    book_name,
                    author,
                    total_books,
                    category,
                    description,
                    book_cover,
                    status
                FROM books
                ORDER BY book_name
                """
            )

        books = cur.fetchall()

    finally:

        con.close()

    return render(
        request,
        "search_books.html",
        {
            "books": books,
            "search": search,
            "result_count": len(books)
        }
    )


# =========================================================
# ADD BOOK
# =========================================================

def add_book(request):

    if not admin_required(request):

        return redirect("admin_login")

    if request.method == "POST":

        book_name = request.POST.get(
            "book_name",
            ""
        ).strip()

        author = request.POST.get(
            "author",
            ""
        ).strip()

        total_books = request.POST.get(
            "total_books",
            "0"
        )

        category = request.POST.get(
            "category",
            "General"
        ).strip()

        description = request.POST.get(
            "description",
            ""
        ).strip()

        book_cover = request.POST.get(
            "book_cover",
            ""
        ).strip()

        try:

            total_books_value = int(
                total_books
            )

        except:

            total_books_value = -1

        if not book_name or not author:

            return render(
                request,
                "add_book.html",
                {
                    "msg":
                    "Book name and author are required."
                }
            )

        if total_books_value < 0:

            return render(
                request,
                "add_book.html",
                {
                    "msg":
                    "Number of books cannot be negative."
                }
            )

        status = (
            "Available"
            if total_books_value > 0
            else
            "Unavailable"
        )

        con = get_connection()
        cur = con.cursor()

        try:

            cur.execute(
                """
                INSERT INTO books
                (
                    book_name,
                    author,
                    total_books,
                    category,
                    description,
                    book_cover,
                    status
                )
                VALUES
                (%s,%s,%s,%s,%s,%s,%s)
                """,
                (
                    book_name,
                    author,
                    total_books_value,
                    category,
                    description,
                    book_cover,
                    status
                )
            )

            con.commit()

        finally:

            con.close()

        return render(
            request,
            "add_book.html",
            {
                "msg":
                "Book Added Successfully"
            }
        )

    return render(
        request,
        "add_book.html"
    )


# =========================================================
# VIEW BOOKS
# =========================================================

def view_books(request):

    if not admin_required(request):

        return redirect("admin_login")

    con = get_connection()
    cur = con.cursor()

    try:

        cur.execute(
            """
            SELECT
                id,
                book_name,
                author,
                total_books,
                category,
                description,
                book_cover,
                status
            FROM books
            ORDER BY id DESC
            """
        )

        books = cur.fetchall()

    finally:

        con.close()

    return render(
        request,
        "view_books.html",
        {
            "books": books
        }
    )


# =========================================================
# EDIT BOOK
# =========================================================

def edit_book(request, book_id):

    if not admin_required(request):

        return redirect("admin_login")

    con = get_connection()
    cur = con.cursor()

    try:

        cur.execute(
            """
            SELECT
                id,
                book_name,
                author,
                total_books,
                category,
                description,
                book_cover,
                status
            FROM books
            WHERE id=%s
            """,
            (book_id,)
        )

        book = cur.fetchone()

        if not book:

            return redirect(
                "view_books"
            )

        if request.method == "POST":

            book_name = request.POST.get(
                "book_name",
                ""
            ).strip()

            author = request.POST.get(
                "author",
                ""
            ).strip()

            total_books = request.POST.get(
                "total_books",
                "0"
            )

            category = request.POST.get(
                "category",
                "General"
            ).strip()

            description = request.POST.get(
                "description",
                ""
            ).strip()

            book_cover = request.POST.get(
                "book_cover",
                ""
            ).strip()

            try:

                total_books_value = int(
                    total_books
                )

            except:

                total_books_value = -1

            if not book_name or not author:

                return render(
                    request,
                    "edit_book.html",
                    {
                        "book": book,
                        "msg":
                        "Book name and author are required."
                    }
                )

            if total_books_value < 0:

                return render(
                    request,
                    "edit_book.html",
                    {
                        "book": book,
                        "msg":
                        "Invalid number of books."
                    }
                )

            status = (
                "Available"
                if total_books_value > 0
                else
                "Unavailable"
            )

            cur.execute(
                """
                UPDATE books
                SET
                    book_name=%s,
                    author=%s,
                    total_books=%s,
                    category=%s,
                    description=%s,
                    book_cover=%s,
                    status=%s
                WHERE id=%s
                """,
                (
                    book_name,
                    author,
                    total_books_value,
                    category,
                    description,
                    book_cover,
                    status,
                    book_id
                )
            )

            con.commit()

            return redirect(
                "view_books"
            )

    finally:

        con.close()

    return render(
        request,
        "edit_book.html",
        {
            "book": book
        }
    )


# =========================================================
# BOOK DETAILS
# =========================================================

def book_details(request, book_id):

    if (
        not student_required(request)
        and
        not admin_required(request)
    ):

        return redirect("login")

    con = get_connection()
    cur = con.cursor()

    try:

        cur.execute(
            """
            SELECT
                id,
                book_name,
                author,
                total_books,
                category,
                description,
                book_cover,
                status
            FROM books
            WHERE id=%s
            """,
            (book_id,)
        )

        book = cur.fetchone()

    finally:

        con.close()

    if not book:

        return redirect(
            "search_books"
        )

    return render(
        request,
        "book_details.html",
        {
            "book": book
        }
    )


# =========================================================
# REMOVE BOOK
# =========================================================

def remove_book(request):

    if not admin_required(request):

        return redirect("admin_login")

    if request.method == "POST":

        book_id = request.POST.get(
            "book_id"
        )

        con = get_connection()
        cur = con.cursor()

        try:

            cur.execute(
                """
                DELETE FROM books
                WHERE id=%s
                """,
                (book_id,)
            )

            con.commit()

        finally:

            con.close()

        return render(
            request,
            "remove_book.html",
            {
                "msg":
                "Book Removed Successfully"
            }
        )

    return render(
        request,
        "remove_book.html"
    )


# =========================================================
# STUDENT MANAGEMENT
# =========================================================

def students(request):

    if not admin_required(request):

        return redirect("admin_login")

    con = None

    students_list = []
    student_count = 0

    try:

        con = get_connection()
        cur = con.cursor()

        cur.execute(
            """
            SELECT
                id,
                username,
                contact,
                email,
                address
            FROM users
            ORDER BY id
            """
        )

        students_list = cur.fetchall()

        cur.execute(
            """
            SELECT COUNT(*)
            FROM users
            """
        )

        student_count = cur.fetchone()[0]

    except Exception as e:

        print(
            "STUDENT MANAGEMENT ERROR:",
            e
        )

    finally:

        if con:
            con.close()

    return render(
        request,
        "students.html",
        {
            "students": students_list,
            "student_count": student_count
        }
    )


# =========================================================
# VIEW STUDENTS
# =========================================================
#
# This alias is added so templates using either
# students OR view_students can work.
#
# =========================================================

def view_students(request):

    return students(request)


# =========================================================
# SEARCH STUDENTS
# =========================================================

def search_students(request):

    if not admin_required(request):

        return redirect("admin_login")

    search = request.GET.get(
        "search",
        ""
    ).strip()

    con = None

    students_list = []
    student_count = 0

    try:

        con = get_connection()
        cur = con.cursor()

        if search:

            value = "%" + search + "%"

            cur.execute(
                """
                SELECT
                    id,
                    username,
                    contact,
                    email,
                    address
                FROM users
                WHERE
                    username LIKE %s
                    OR contact LIKE %s
                    OR email LIKE %s
                    OR address LIKE %s
                ORDER BY id
                """,
                (
                    value,
                    value,
                    value,
                    value
                )
            )

        else:

            cur.execute(
                """
                SELECT
                    id,
                    username,
                    contact,
                    email,
                    address
                FROM users
                ORDER BY id
                """
            )

        students_list = cur.fetchall()

        cur.execute(
            """
            SELECT COUNT(*)
            FROM users
            """
        )

        student_count = cur.fetchone()[0]

    except Exception as e:

        print(
            "SEARCH STUDENTS ERROR:",
            e
        )

    finally:

        if con:
            con.close()

    return render(
        request,
        "search.html",
        {
            "students": students_list,
            "student_count": student_count,
            "search": search,
            "result_count": len(students_list)
        }
    )


# =========================================================
# STUDENT PROFILE
# =========================================================

def student_profile(request):

    if not student_required(request):

        return redirect("login")

    student_id = request.session.get(
        "student_id"
    )

    con = get_connection()
    cur = con.cursor()

    try:

        if request.method == "POST":

            contact = request.POST.get(
                "contact",
                ""
            )

            email = request.POST.get(
                "email",
                ""
            )

            address = request.POST.get(
                "address",
                ""
            )

            cur.execute(
                """
                UPDATE users
                SET
                    contact=%s,
                    email=%s,
                    address=%s
                WHERE id=%s
                """,
                (
                    contact,
                    email,
                    address,
                    student_id
                )
            )

            con.commit()

            msg = "Profile Updated Successfully"

        else:

            msg = None

        cur.execute(
            """
            SELECT
                id,
                username,
                contact,
                email,
                address
            FROM users
            WHERE id=%s
            """,
            (student_id,)
        )

        student = cur.fetchone()

    finally:

        con.close()

    return render(
        request,
        "student_profile.html",
        {
            "student": student,
            "msg": msg
        }
    )


# =========================================================
# CHANGE PASSWORD
# =========================================================

def change_password(request):

    if not student_required(request):

        return redirect("login")

    student_id = request.session.get(
        "student_id"
    )

    if request.method == "POST":

        old_password = request.POST.get(
            "old_password",
            ""
        )

        new_password = request.POST.get(
            "new_password",
            ""
        )

        confirm_password = request.POST.get(
            "confirm_password",
            ""
        )

        if not new_password:

            return render(
                request,
                "change_password.html",
                {
                    "msg":
                    "New password is required."
                }
            )

        if new_password != confirm_password:

            return render(
                request,
                "change_password.html",
                {
                    "msg":
                    "New passwords do not match."
                }
            )

        con = get_connection()
        cur = con.cursor()

        try:

            cur.execute(
                """
                SELECT password
                FROM users
                WHERE id=%s
                """,
                (student_id,)
            )

            user = cur.fetchone()

            if (
                not user
                or
                str(user[0]) != str(old_password)
            ):

                return render(
                    request,
                    "change_password.html",
                    {
                        "msg":
                        "Current password is incorrect."
                    }
                )

            cur.execute(
                """
                UPDATE users
                SET password=%s
                WHERE id=%s
                """,
                (
                    new_password,
                    student_id
                )
            )

            con.commit()

        finally:

            con.close()

        return render(
            request,
            "change_password.html",
            {
                "msg":
                "Password Changed Successfully"
            }
        )

    return render(
        request,
        "change_password.html"
    )


# =========================================================
# REMOVE STUDENT
# =========================================================

def remove_student(request):

    if not admin_required(request):

        return redirect("admin_login")

    if request.method != "POST":

        return redirect(
            "view_students"
        )

    student_id = request.POST.get(
        "student_id"
    )

    if not student_id:

        return redirect(
            "view_students"
        )

    con = None

    try:

        con = get_connection()
        cur = con.cursor()

        cur.execute(
            """
            DELETE FROM users
            WHERE id=%s
            """,
            (student_id,)
        )

        con.commit()

    except Exception as e:

        if con:
            con.rollback()

        print(
            "REMOVE STUDENT ERROR:",
            e
        )

    finally:

        if con:
            con.close()

    return redirect(
        "view_students"
    )


# =========================================================
# BOOK SLOT
# =========================================================

def book_slot(request):

    if not student_required(request):

        return redirect("login")

    student_id = request.session.get(
        "student_id"
    )

    con = get_connection()
    cur = con.cursor()

    try:

        if request.method == "POST":

            book_id = request.POST.get(
                "book_id"
            )

            booking_date = request.POST.get(
                "booking_date"
            )

            time_slot = request.POST.get(
                "time_slot"
            )

            cur.execute(
                """
                SELECT
                    id,
                    book_name,
                    author,
                    total_books
                FROM books
                WHERE id=%s
                """,
                (book_id,)
            )

            book = cur.fetchone()

            if not book:

                return render(
                    request,
                    "book_slot.html",
                    {
                        "msg":
                        "Book not found."
                    }
                )

            if book[3] <= 0:

                return render(
                    request,
                    "book_slot.html",
                    {
                        "msg":
                        "No copies available."
                    }
                )

            try:

                if booking_date:

                    booking_date_object = datetime.strptime(
                        booking_date,
                        "%Y-%m-%d"
                    ).date()

                else:

                    booking_date_object = datetime.now().date()

            except:

                booking_date_object = datetime.now().date()

            due_date = (
                booking_date_object
                +
                timedelta(days=BOOKING_DAYS)
            )

            cur.execute(
                """
                INSERT INTO bookings
                (
                    student_id,
                    book_id,
                    booking_date,
                    time_slot,
                    due_date,
                    status,
                    fine
                )
                VALUES
                (%s,%s,%s,%s,%s,%s,%s)
                """,
                (
                    student_id,
                    book_id,
                    booking_date_object,
                    time_slot,
                    due_date,
                    "Booked",
                    Decimal("0.00")
                )
            )

            cur.execute(
                """
                UPDATE books
                SET
                    total_books =
                        total_books - 1,

                    status =
                        CASE
                            WHEN total_books - 1 > 0
                            THEN 'Available'
                            ELSE 'Unavailable'
                        END

                WHERE id=%s
                AND total_books > 0
                """,
                (book_id,)
            )

            con.commit()

            cur.execute(
                """
                SELECT
                    id,
                    book_name,
                    author,
                    total_books
                FROM books
                ORDER BY id
                """
            )

            books = cur.fetchall()

            return render(
                request,
                "book_slot.html",
                {
                    "books": books,
                    "msg":
                    "Book Slot Successfully Booked",
                    "due_date": due_date
                }
            )

        cur.execute(
            """
            SELECT
                id,
                book_name,
                author,
                total_books
            FROM books
            WHERE total_books > 0
            ORDER BY id
            """
        )

        books = cur.fetchall()

    finally:

        con.close()

    return render(
        request,
        "book_slot.html",
        {
            "books": books
        }
    )


# =========================================================
# MY BOOKINGS
# =========================================================

def my_bookings(request):

    if not student_required(request):

        return redirect("login")

    student_id = request.session.get(
        "student_id"
    )

    con = get_connection()
    cur = con.cursor()

    updated_bookings = []

    total_fine = Decimal("0.00")

    today = datetime.now().date()

    try:

        cur.execute(
            """
            SELECT
                bookings.id,
                books.book_name,
                books.author,
                bookings.booking_date,
                bookings.time_slot,
                bookings.due_date,
                bookings.status,
                bookings.fine
            FROM bookings
            JOIN books
                ON bookings.book_id = books.id
            WHERE bookings.student_id=%s
            ORDER BY
                bookings.booking_date DESC,
                bookings.id DESC
            """,
            (student_id,)
        )

        rows = cur.fetchall()

        for row in rows:

            booking_id = row[0]
            book_name = row[1]
            author = row[2]
            booking_date = row[3]
            time_slot = row[4]
            due_date = row[5]
            database_status = row[6]

            database_fine = (
                row[7]
                if row[7] is not None
                else Decimal("0.00")
            )

            if hasattr(booking_date, "date"):

                booking_date = booking_date.date()

            if hasattr(due_date, "date"):

                due_date = due_date.date()

            if database_status == "Returned":

                status = "Returned"
                fine = database_fine

            elif database_status == "Cancelled":

                status = "Cancelled"
                fine = Decimal("0.00")

            elif due_date and today > due_date:

                status = "Overdue"

                overdue_days = (
                    today - due_date
                ).days

                fine = (
                    Decimal(overdue_days)
                    *
                    FINE_PER_DAY
                )

            else:

                status = "Booked"
                fine = Decimal("0.00")

            cur.execute(
                """
                UPDATE bookings
                SET fine=%s
                WHERE id=%s
                """,
                (
                    fine,
                    booking_id
                )
            )

            total_fine += fine

            updated_bookings.append(
                {
                    "id": booking_id,
                    "book_name": book_name,
                    "author": author,
                    "booking_date": booking_date,
                    "time_slot": time_slot,
                    "due_date": due_date,
                    "status": status,
                    "fine": fine
                }
            )

        con.commit()

    finally:

        con.close()

    return render(
        request,
        "my_bookings.html",
        {
            "bookings": updated_bookings,
            "total_fine": total_fine,
            "today": today
        }
    )


# =========================================================
# RETURN BOOK
# =========================================================

def return_book(request):

    if not student_required(request):

        return redirect("login")

    if request.method != "POST":

        return redirect(
            "my_bookings"
        )

    booking_id = request.POST.get(
        "booking_id"
    )

    student_id = request.session.get(
        "student_id"
    )

    if not booking_id:

        return redirect(
            "my_bookings"
        )

    con = get_connection()
    cur = con.cursor()

    try:

        cur.execute(
            """
            SELECT
                book_id,
                due_date,
                status
            FROM bookings
            WHERE id=%s
            AND student_id=%s
            """,
            (
                booking_id,
                student_id
            )
        )

        booking = cur.fetchone()

        if booking:

            book_id = booking[0]
            due_date = booking[1]
            status = booking[2]

            if status not in (
                "Returned",
                "Cancelled"
            ):

                if hasattr(due_date, "date"):

                    due_date = due_date.date()

                if (
                    due_date
                    and
                    datetime.now().date() > due_date
                ):

                    overdue_days = (
                        datetime.now().date()
                        -
                        due_date
                    ).days

                    fine = (
                        Decimal(overdue_days)
                        *
                        FINE_PER_DAY
                    )

                else:

                    fine = Decimal("0.00")

                cur.execute(
                    """
                    UPDATE bookings
                    SET
                        status='Returned',
                        fine=%s
                    WHERE id=%s
                    AND student_id=%s
                    """,
                    (
                        fine,
                        booking_id,
                        student_id
                    )
                )

                cur.execute(
                    """
                    UPDATE books
                    SET
                        total_books =
                            total_books + 1,
                        status='Available'
                    WHERE id=%s
                    """,
                    (book_id,)
                )

                con.commit()

    except Exception as e:

        con.rollback()

        print(
            "RETURN ERROR:",
            e
        )

    finally:

        con.close()

    return redirect(
        "my_bookings"
    )


# =========================================================
# CANCEL BOOKING
# =========================================================

def cancel_booking(request):

    if not student_required(request):

        return redirect("login")

    if request.method != "POST":

        return redirect(
            "my_bookings"
        )

    booking_id = request.POST.get(
        "booking_id"
    )

    student_id = request.session.get(
        "student_id"
    )

    if not booking_id:

        return redirect(
            "my_bookings"
        )

    con = get_connection()
    cur = con.cursor()

    try:

        cur.execute(
            """
            SELECT
                book_id,
                status
            FROM bookings
            WHERE id=%s
            AND student_id=%s
            """,
            (
                booking_id,
                student_id
            )
        )

        booking = cur.fetchone()

        if booking:

            book_id = booking[0]
            status = booking[1]

            if status not in (
                "Returned",
                "Cancelled"
            ):

                cur.execute(
                    """
                    UPDATE bookings
                    SET
                        status='Cancelled',
                        fine=0
                    WHERE id=%s
                    AND student_id=%s
                    """,
                    (
                        booking_id,
                        student_id
                    )
                )

                cur.execute(
                    """
                    UPDATE books
                    SET
                        total_books =
                            total_books + 1,
                        status='Available'
                    WHERE id=%s
                    """,
                    (book_id,)
                )

                con.commit()

    except Exception as e:

        con.rollback()

        print(
            "CANCEL ERROR:",
            e
        )

    finally:

        con.close()

    return redirect(
        "my_bookings"
    )


# =========================================================
# BOOKING HISTORY
# =========================================================

def booking_history(request):

    if not student_required(request):

        return redirect("login")

    student_id = request.session.get(
        "student_id"
    )

    con = get_connection()
    cur = con.cursor()

    try:

        cur.execute(
            """
            SELECT
                bookings.id,
                books.book_name,
                books.author,
                bookings.booking_date,
                bookings.time_slot,
                bookings.due_date,
                bookings.status,
                bookings.fine
            FROM bookings
            JOIN books
                ON bookings.book_id = books.id
            WHERE bookings.student_id=%s
            AND bookings.status IN
            ('Returned','Cancelled')
            ORDER BY bookings.booking_date DESC
            """,
            (student_id,)
        )

        bookings = cur.fetchall()

    finally:

        con.close()

    return render(
        request,
        "booking_history.html",
        {
            "bookings": bookings
        }
    )


# =========================================================
# STUDENT NOTIFICATIONS
# =========================================================

def student_notifications(request):

    if not student_required(request):

        return redirect("login")

    student_id = request.session.get(
        "student_id"
    )

    con = get_connection()
    cur = con.cursor()

    notifications = []

    today = datetime.now().date()

    try:

        cur.execute(
            """
            SELECT
                bookings.id,
                books.book_name,
                bookings.booking_date,
                bookings.due_date,
                bookings.status,
                bookings.fine
            FROM bookings
            JOIN books
                ON bookings.book_id = books.id
            WHERE bookings.student_id=%s
            ORDER BY
                bookings.booking_date DESC,
                bookings.id DESC
            """,
            (student_id,)
        )

        rows = cur.fetchall()

        for row in rows:

            booking_id = row[0]
            book_name = row[1]
            booking_date = row[2]
            due_date = row[3]
            database_status = row[4]

            database_fine = (
                row[5]
                if row[5] is not None
                else Decimal("0.00")
            )

            if hasattr(booking_date, "date"):

                booking_date = booking_date.date()

            if hasattr(due_date, "date"):

                due_date = due_date.date()

            if database_status == "Returned":

                status = "Returned"
                current_fine = database_fine
                notification_type = "Book Returned"

            elif database_status == "Cancelled":

                status = "Cancelled"
                current_fine = Decimal("0.00")
                notification_type = "Booking Cancelled"

            elif due_date and today > due_date:

                status = "Overdue"

                overdue_days = (
                    today - due_date
                ).days

                current_fine = (
                    Decimal(overdue_days)
                    *
                    FINE_PER_DAY
                )

                notification_type = "Book Overdue"

            else:

                status = "Booked"
                current_fine = Decimal("0.00")
                notification_type = "Book Booking"

            cur.execute(
                """
                UPDATE bookings
                SET fine=%s
                WHERE id=%s
                """,
                (
                    current_fine,
                    booking_id
                )
            )

            notifications.append(
                {
                    "id": booking_id,
                    "book_name": book_name,
                    "booking_date": booking_date,
                    "due_date": due_date,
                    "status": status,
                    "fine": current_fine,
                    "notification_type":
                        notification_type
                }
            )

        con.commit()

    finally:

        con.close()

    return render(
        request,
        "student_notifications.html",
        {
            "notifications": notifications,
            "notification_count":
                len(notifications),
            "today": today
        }
    )


# =========================================================
# ADMIN NOTIFICATIONS
# =========================================================

def admin_notifications(request):

    if not admin_required(request):

        return redirect("admin_login")

    con = get_connection()
    cur = con.cursor()

    notifications = []

    today = datetime.now().date()

    try:

        cur.execute(
            """
            SELECT
                bookings.id,
                users.username,
                books.book_name,
                bookings.booking_date,
                bookings.due_date,
                bookings.status,
                bookings.fine
            FROM bookings
            INNER JOIN users
                ON bookings.student_id = users.id
            INNER JOIN books
                ON bookings.book_id = books.id
            ORDER BY
                bookings.booking_date DESC,
                bookings.id DESC
            """
        )

        rows = cur.fetchall()

        for row in rows:

            booking_id = row[0]
            username = row[1]
            book_name = row[2]
            booking_date = row[3]
            due_date = row[4]
            database_status = row[5]

            database_fine = (
                row[6]
                if row[6] is not None
                else Decimal("0.00")
            )

            if hasattr(booking_date, "date"):

                booking_date = booking_date.date()

            if hasattr(due_date, "date"):

                due_date = due_date.date()

            if database_status == "Returned":

                status = "Returned"
                current_fine = database_fine
                notification_type = "Returned"

            elif database_status == "Cancelled":

                status = "Cancelled"
                current_fine = Decimal("0.00")
                notification_type = "Cancelled"

            elif database_status == "Booked":

                if due_date and today > due_date:

                    status = "Overdue"

                    overdue_days = (
                        today - due_date
                    ).days

                    current_fine = (
                        Decimal(overdue_days)
                        *
                        FINE_PER_DAY
                    )

                    notification_type = "Overdue"

                else:

                    status = "Booked"
                    current_fine = Decimal("0.00")
                    notification_type = "New Booking"

            else:

                status = database_status
                current_fine = database_fine
                notification_type = database_status

            cur.execute(
                """
                UPDATE bookings
                SET fine=%s
                WHERE id=%s
                """,
                (
                    current_fine,
                    booking_id
                )
            )

            notifications.append(
                {
                    "id": booking_id,
                    "username": username,
                    "book_name": book_name,
                    "booking_date": booking_date,
                    "due_date": due_date,
                    "database_status":
                        database_status,
                    "status": status,
                    "fine": current_fine,
                    "notification_type":
                        notification_type
                }
            )

        con.commit()

    except Exception as e:

        con.rollback()

        print(
            "ADMIN NOTIFICATION ERROR:",
            e
        )

    finally:

        con.close()

    return render(
        request,
        "admin_notifications.html",
        {
            "notifications": notifications,
            "notification_count":
                len(notifications),
            "today": today
        }
    )


# =========================================================
# VIEW ALL BOOKINGS - ADMIN
# =========================================================

def view_bookings(request):

    if not admin_required(request):

        return redirect("admin_login")

    con = get_connection()
    cur = con.cursor()

    updated_bookings = []

    try:

        cur.execute(
            """
            SELECT
                bookings.id,
                users.username,
                books.book_name,
                bookings.booking_date,
                bookings.time_slot,
                bookings.due_date,
                bookings.status,
                bookings.fine
            FROM bookings
            JOIN users
                ON bookings.student_id = users.id
            JOIN books
                ON bookings.book_id = books.id
            ORDER BY
                bookings.booking_date DESC,
                bookings.id DESC
            """
        )

        rows = cur.fetchall()

        for row in rows:

            booking_id = row[0]
            due_date = row[5]
            status = row[6]

            if hasattr(due_date, "date"):

                due_date = due_date.date()

            if (
                status == "Cancelled"
                or
                status == "Returned"
            ):

                fine = (
                    row[7]
                    if row[7] is not None
                    else Decimal("0.00")
                )

            else:

                if (
                    due_date
                    and
                    datetime.now().date() > due_date
                ):

                    overdue_days = (
                        datetime.now().date()
                        -
                        due_date
                    ).days

                    fine = (
                        Decimal(overdue_days)
                        *
                        FINE_PER_DAY
                    )

                else:

                    fine = Decimal("0.00")

            cur.execute(
                """
                UPDATE bookings
                SET fine=%s
                WHERE id=%s
                """,
                (
                    fine,
                    booking_id
                )
            )

            booking_list = list(row)

            booking_list[5] = due_date
            booking_list[7] = fine

            updated_bookings.append(
                tuple(booking_list)
            )

        con.commit()

    finally:

        con.close()

    return render(
        request,
        "view_bookings.html",
        {
            "bookings":
                updated_bookings
        }
    )


# =========================================================
# LOGOUT
# =========================================================

def logout(request):

    request.session.flush()

    return redirect(
        "index"
    )