# Library Management System

A complete **Library Management System** developed using **Django, Python, MySQL, HTML, CSS, Bootstrap, JavaScript, and PyMySQL**.

The system provides separate interfaces for **Students** and **Administrators** and supports book management, booking, due-date tracking, overdue detection, automatic fines, notifications, student management, book covers, search, booking history, and responsive UI.

---

## 1. Project Overview

### Student Module

Students can:

* Create an account
* Login/logout
* View available books
* Search books
* Browse book categories
* View book details
* View book covers
* Book books
* Check due dates
* View overdue status
* View fines
* Return books
* Cancel bookings
* View booking history
* Receive notifications
* Update profile
* Change password

### Administrator Module

Administrators can:

* Login/logout
* View dashboard statistics
* Add books
* View books
* Edit books
* Remove books
* Search books
* Manage book covers
* View students
* Search students
* Remove students
* View bookings
* Monitor overdue books
* Monitor fines
* Receive booking notifications

---

## 2. Technologies Used

| Technology       | Purpose                   |
| ---------------- | ------------------------- |
| Python           | Backend programming       |
| Django 4.2.1     | Web framework             |
| MySQL            | Database                  |
| PyMySQL          | MySQL connection          |
| HTML5            | Page structure            |
| CSS3             | Styling                   |
| Bootstrap 5      | Responsive UI             |
| JavaScript       | Client-side functionality |
| Django Templates | Dynamic web pages         |

---

## 3. Main Features

### Student Features

* Student registration
* Student login/logout
* Student dashboard
* Available books
* Book categories
* Book search
* Book details
* Book covers
* Book booking
* Due-date calculation
* Overdue detection
* Automatic fine calculation
* Return book
* Cancel booking
* Booking history
* Notifications
* Profile management
* Password change

### Admin Features

* Admin login/logout
* Admin dashboard
* Statistics
* Add books
* Edit books
* Delete books
* Search books
* Book cover management
* Student management
* Student search
* Booking monitoring
* Overdue monitoring
* Fine monitoring
* Admin notifications

---

## 4. Due-Date and Fine System

The project uses a **7-day borrowing period**.

```text
BOOKING_DAYS = 7
FINE_PER_DAY = ₹10
```

Formula:

```text
Due Date = Booking Date + 7 Days

Fine = Overdue Days × ₹10
```

Example:

```text
Due Date: 10 August
Today:    13 August

Overdue Days = 3

Fine = 3 × ₹10
     = ₹30
```

---

## 5. Booking Workflow

```text
Student Login
      ↓
Available Books
      ↓
Book Details
      ↓
Book Booking
      ↓
Due Date Generated
      ↓
My Bookings
      ↓
Due Date Reached
      ↓
Overdue Detection
      ↓
Fine Calculation
      ↓
Return / Cancel
      ↓
Booking History
      ↓
Notification
```

---

## 6. Inventory Workflow

When a student books a book:

```text
Available Copies - 1
```

When a student returns a book:

```text
Available Copies + 1
```

When a student cancels a booking:

```text
Available Copies + 1
```

The availability status is updated automatically.

---

## 7. Database

Database name:

```text
student
```

Main tables:

```text
users
books
bookings
```

### Users

```text
id
username
password
contact
email
address
```

### Books

```text
id
book_name
author
total_books
category
description
book_cover
status
```

### Bookings

```text
id
student_id
book_id
booking_date
time_slot
due_date
status
fine
```

Relationships:

```text
users.id
   ↓
bookings.student_id

books.id
   ↓
bookings.book_id
```

---

## 8. Project Structure

```text
LibraryManagementSystem/
│
├── manage.py
│
├── project/
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── __init__.py
│
├── library/
│   ├── views.py
│   ├── urls.py
│   ├── models.py
│   ├── admin.py
│   └── __init__.py
│
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── login.html
│   ├── signup.html
│   ├── student_home.html
│   ├── student_notifications.html
│   ├── student_profile.html
│   ├── change_password.html
│   ├── available_books.html
│   ├── book_categories.html
│   ├── book_category.html
│   ├── book_details.html
│   ├── book_slot.html
│   ├── my_bookings.html
│   ├── booking_history.html
│   ├── admin_login.html
│   ├── admin_home.html
│   ├── admin_statistics.html
│   ├── admin_notifications.html
│   ├── view_books.html
│   ├── add_book.html
│   ├── edit_book.html
│   ├── remove_book.html
│   ├── view_bookings.html
│   ├── students.html
│   ├── search_books.html
│   ├── search_students.html
│   └── remove_student.html
│
└── README.md
```

---

# 9. HTML Template Links

Click each output to open the corresponding HTML file.

### Common Pages

**Output 1 — Base Template**
[Open output1 — base.html](templates/base.html)

**Output 2 — Home Page**
[Open output2 — index.html](templates/index.html)

**Output 3 — Student Login**
[Open output3 — login.html](templates/login.html)

**Output 4 — Student Signup**
[Open output4 — signup.html](templates/signup.html)

---

### Student Pages

**Output 5 — Student Dashboard**
[Open output5 — student_home.html](templates/student_home.html)

**Output 6 — Student Notifications**
[Open output6 — student_notifications.html](templates/student_notifications.html)

**Output 7 — Student Profile**
[Open output7 — student_profile.html](templates/student_profile.html)

**Output 8 — Change Password**
[Open output8 — change_password.html](templates/change_password.html)

**Output 9 — Available Books**
[Open output9 — available_books.html](templates/available_books.html)

**Output 10 — Book Categories**
[Open output10 — book_categories.html](templates/book_categories.html)

**Output 11 — Book Category**
[Open output11 — book_category.html](templates/book_category.html)

**Output 12 — Book Details**
[Open output12 — book_details.html](templates/book_details.html)

**Output 13 — Book Slot**
[Open output13 — book_slot.html](templates/book_slot.html)

**Output 14 — My Bookings**
[Open output14 — my_bookings.html](templates/my_bookings.html)

**Output 15 — Booking History**
[Open output15 — booking_history.html](templates/booking_history.html)

---

### Admin Pages

**Output 16 — Admin Login**
[Open output16 — admin_login.html](templates/admin_login.html)

**Output 17 — Admin Dashboard**
[Open output17 — admin_home.html](templates/admin_home.html)

**Output 18 — Admin Statistics**
[Open output18 — admin_statistics.html](templates/admin_statistics.html)

**Output 19 — Admin Notifications**
[Open output19 — admin_notifications.html](templates/admin_notifications.html)

**Output 20 — View Books**
[Open output20 — view_books.html](templates/view_books.html)

**Output 21 — Add Book**
[Open output21 — add_book.html](templates/add_book.html)

**Output 22 — Edit Book**
[Open output22 — edit_book.html](templates/edit_book.html)

**Output 23 — Remove Book**
[Open output23 — remove_book.html](templates/remove_book.html)

**Output 24 — View Bookings**
[Open output24 — view_bookings.html](templates/view_bookings.html)

**Output 25 — Students**
[Open output25 — students.html](templates/students.html)

**Output 26 — Search Books**
[Open output26 — search_books.html](templates/search_books.html)

**Output 27 — Search Students**
[Open output27 — search_students.html](templates/search_students.html)

**Output 28 — Remove Student**
[Open output28 — remove_student.html](templates/remove_student.html)

---

# 10. Installation

Install Django:

```bash
pip install django==4.2.1
```

Install PyMySQL:

```bash
pip install pymysql
```

Verify Django:

```bash
python -m django --version
```

Expected:

```text
4.2.1
```

---

# 11. MySQL Setup

Create the database:

```sql
CREATE DATABASE student;
```

Configure the MySQL connection according to your local MySQL username and password.

**Credentials are intentionally not included in this README.**

Do not publish database passwords, administrator credentials, or other secrets in source code or documentation.

---

# 12. Running the Project

Open Command Prompt and navigate to the project directory:

```bash
cd C:\Users\Administrator\Desktop\LibraryManagementSystem
```

Run the Django server:

```bash
python manage.py runserver
```

Open:

```text
http://127.0.0.1:8000/
```

---

# 13. Security

Administrator and database usernames/passwords have been **removed from this documentation**.

For production deployment:

* Store credentials in environment variables.
* Never commit passwords to GitHub.
* Use Django's password hashing.
* Use secure session configuration.
* Use separate database credentials with limited permissions.
* Change any development credentials before deployment.

---

# 14. Security and Session Protection

Student-only pages use:

```text
student_required(request)
```

Admin-only pages use:

```text
admin_required(request)
```

Unauthorized users are redirected to the appropriate login page.

---

# 15. Responsive UI

The application uses Bootstrap and responsive CSS.

Supported devices:

```text
Desktop
Laptop
Tablet
Mobile
```

Book cards automatically adjust according to screen size.

```text
Desktop → 4 cards per row
Tablet  → 2 cards per row
Mobile  → 1 card per row
```

---

# 16. Error Handling

The project handles common errors including:

* Duplicate usernames
* Missing book name
* Missing author
* Invalid book quantity
* Negative book quantity
* Invalid password
* Password mismatch
* Book not found
* No available copies
* Invalid booking information
* Unauthorized access

---

# 17. Common Problems

### TemplateDoesNotExist

Example:

```text
TemplateDoesNotExist at /login/
base.html
```

Solution:

Ensure:

```text
templates/
    base.html
```

exists and that Django's template configuration points to the correct templates directory.

---

### Django Session Table Error

If you receive:

```text
no such table: django_session
```

run:

```bash
python manage.py migrate
```

Then restart the server.

---

### Jupyter Error

If Python reports:

```text
No module named jupyter
```

install Jupyter:

```bash
python -m pip install jupyter
```

Run:

```bash
python -m jupyter notebook
```

---

### Book Cover Not Showing

Check:

```sql
SELECT id, book_name, book_cover
FROM books;
```

Make sure the `book_cover` field contains a valid image URL.

---

# 18. Student Testing Checklist

* [ ] Signup works
* [ ] Duplicate username is rejected
* [ ] Login works
* [ ] Invalid login is rejected
* [ ] Dashboard loads
* [ ] Available books display
* [ ] Book covers display
* [ ] Missing covers show fallback
* [ ] Search works
* [ ] Categories work
* [ ] Book details work
* [ ] Booking works
* [ ] Due date is generated
* [ ] My Bookings works
* [ ] Overdue status works
* [ ] Fine calculation works
* [ ] Return works
* [ ] Cancel works
* [ ] Booking history works
* [ ] Notifications work
* [ ] Profile update works
* [ ] Password change works
* [ ] Logout works

---

# 19. Admin Testing Checklist

* [ ] Admin login works
* [ ] Admin dashboard works
* [ ] Statistics work
* [ ] Add book works
* [ ] View books works
* [ ] Edit book works
* [ ] Delete book works
* [ ] Search books works
* [ ] Book covers work
* [ ] View students works
* [ ] Search students works
* [ ] Remove student works
* [ ] View bookings works
* [ ] New booking notification works
* [ ] Overdue notification works
* [ ] Returned notification works
* [ ] Cancelled notification works
* [ ] Fine displays correctly
* [ ] Admin logout works

---

# 20. Complete Project Workflow

```text
                 LIBRARY MANAGEMENT SYSTEM
                           │
             ┌─────────────┴─────────────┐
             │                           │
         STUDENT                       ADMIN
             │                           │
      ┌──────┴──────┐             ┌──────┴──────┐
      │             │             │             │
    Books        Bookings       Books        Students
      │             │             │             │
   Search       Due Date       Add/Edit      Search
   Category     Overdue        Remove        Manage
   Details      Fine           Cover         Bookings
   Cover        Return         Search        Statistics
                Cancel
                History
                Notifications
```

---

# 21. Final Project Status

| Module                | Status    |
| --------------------- | --------- |
| Core System           | Completed |
| Student Module        | Completed |
| Admin Module          | Completed |
| Book Management       | Completed |
| Booking Management    | Completed |
| Due-Date System       | Completed |
| Overdue & Fine System | Completed |
| Student Notifications | Completed |
| Admin Notifications   | Completed |
| Book Covers           | Completed |
| Search                | Completed |
| Responsive UI         | Completed |
| Booking History       | Completed |

---

# 22. Future Improvements

Possible future enhancements:

* Secure password hashing
* Django ORM
* Role-based authentication
* Email notifications
* SMS notifications
* Online fine payment
* PDF reports
* Excel export
* Book cover file upload
* Pagination
* REST API
* Barcode/QR-code scanning
* Multiple administrator accounts
* Reservation/waitlist system
* Audit logs
* Cloud deployment

---

# 23. Conclusion

The **Library Management System** provides a complete web-based solution for managing:

```text
Books
Students
Bookings
Returns
Due Dates
Overdue Books
Fines
Notifications
Book Inventory
Booking History
```



**The Library Management System is ready for final testing, screenshots, project presentation, and academic documentation.**
