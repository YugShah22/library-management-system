from django.contrib import admin
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("", views.index, name="home"),
    path("login/", views.login_view, name="login"),
    path("register/", views.register, name="register"),
    path("catalog/",views.catalog,name="catalog"),
    path('borrow/<int:book_id>/', views.borrow_book, name='borrow_book'),
    path('reserve/<int:book_id>/', views.reserve_book, name='reserve_book'),
    path('return/<int:borrow_id>/', views.return_book, name='return_book'),
    path('dashboard/', views.user_dashboard, name='user_dashboard'),
    path('cancel_reservation/<int:reservation_id>/', views.cancel_reservation, name='cancel_reservation'),
    path("logout/", views.logout_view, name="logout"),
]


