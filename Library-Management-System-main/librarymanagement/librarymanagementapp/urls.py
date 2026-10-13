from django.urls import path
from . import views


urlpatterns = [

    # =====================================================
    # HOME
    # =====================================================

    path(
        "",
        views.index,
        name="index"
    ),


    # =====================================================
    # STUDENT AUTHENTICATION
    # =====================================================

    path(
        "signup/",
        views.signup,
        name="signup"
    ),

    path(
        "login/",
        views.login,
        name="login"
    ),

    path(
        "logout/",
        views.logout,
        name="logout"
    ),


    # =====================================================
    # STUDENT DASHBOARD
    # =====================================================

    path(
        "student-home/",
        views.student_home,
        name="student_home"
    ),

    path(
        "student-profile/",
        views.student_profile,
        name="student_profile"
    ),

    path(
        "change-password/",
        views.change_password,
        name="change_password"
    ),


    # =====================================================
    # STUDENT BOOKS
    # =====================================================

    path(
        "available-books/",
        views.available_books,
        name="available_books"
    ),

    path(
        "book-categories/",
        views.book_categories,
        name="book_categories"
    ),

    path(
        "book-category/<str:category>/",
        views.book_category,
        name="book_category"
    ),

    path(
        "search-books/",
        views.search_books,
        name="search_books"
    ),

    path(
        "book-details/<int:book_id>/",
        views.book_details,
        name="book_details"
    ),


    # =====================================================
    # STUDENT BOOKING
    # =====================================================

    path(
        "book-slot/",
        views.book_slot,
        name="book_slot"
    ),

    path(
        "my-bookings/",
        views.my_bookings,
        name="my_bookings"
    ),

    path(
        "return-book/",
        views.return_book,
        name="return_book"
    ),

    path(
        "cancel-booking/",
        views.cancel_booking,
        name="cancel_booking"
    ),

    path(
        "booking-history/",
        views.booking_history,
        name="booking_history"
    ),

    path(
        "student-notifications/",
        views.student_notifications,
        name="student_notifications"
    ),


    # =====================================================
    # ADMIN AUTHENTICATION
    # =====================================================

    path(
        "admin-login/",
        views.admin_login,
        name="admin_login"
    ),


    # =====================================================
    # ADMIN DASHBOARD
    # =====================================================

    path(
        "admin-home/",
        views.admin_home,
        name="admin_home"
    ),

    path(
        "admin-statistics/",
        views.admin_statistics,
        name="admin_statistics"
    ),

    path(
        "admin-notifications/",
        views.admin_notifications,
        name="admin_notifications"
    ),


    # =====================================================
    # ADMIN BOOK MANAGEMENT
    # =====================================================

    path(
        "add-book/",
        views.add_book,
        name="add_book"
    ),

    path(
        "view-books/",
        views.view_books,
        name="view_books"
    ),

    path(
        "edit-book/<int:book_id>/",
        views.edit_book,
        name="edit_book"
    ),

    path(
        "remove-book/",
        views.remove_book,
        name="remove_book"
    ),


    # =====================================================
    # ADMIN STUDENT MANAGEMENT
    # =====================================================

    # Main Student Management page
    path(
        "students/",
        views.students,
        name="students"
    ),

    # Alias used by existing templates
    path(
        "view-students/",
        views.students,
        name="view_students"
    ),

    # Search students
    path(
        "search-students/",
        views.search_students,
        name="search_students"
    ),

    # Remove student
    path(
        "remove-student/",
        views.remove_student,
        name="remove_student"
    ),


    # =====================================================
    # ADMIN BOOKINGS
    # =====================================================

    path(
        "view-bookings/",
        views.view_bookings,
        name="view_bookings"
    ),

]