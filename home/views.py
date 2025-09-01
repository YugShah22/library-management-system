from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login as auth_login
from django.contrib import messages 
from django.shortcuts import render, get_object_or_404, redirect
from .models import Book, Borrow, Reservation
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout


def index(request):
    return render(request, 'index.html')

def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            messages.success(request, f'Account created for {user.username}!') 
            return redirect("home")
    else:
        form = UserCreationForm()
    return render(request, "register.html", {"form": form})

def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            messages.success(request, f'Welcome back, {user.username}!') 
            return redirect("catalog")
        else:
            messages.error(request, 'Invalid username or password.') 
            return render(request, "login.html") 
    
    return render(request, "login.html")

from django.shortcuts import render
from .models import Book

def catalog(request):
    books = Book.objects.all()
    query = request.GET.get("q")
    sort = request.GET.get("sort")

    if query:
        books = books.filter(title__icontains=query)
    if sort == "title":
        books = books.order_by("title")
    elif sort == "author":
        books = books.order_by("author")

    return render(request, "catalog.html", {"books": books, "query": query, "sort": sort})

@login_required
def borrow_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if book.is_available:
        Borrow.objects.create(user=request.user, book=book)
        book.is_available = False
        book.save()
    return redirect('catalog')  # go back to catalog

@login_required
def reserve_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if not book.is_available:
        # add reservation only if book not available
        Reservation.objects.create(user=request.user, book=book)
    return redirect('catalog')

@login_required
def user_dashboard(request):
    borrowed_books = Borrow.objects.filter(user=request.user, returned=False)
    reserved_books = Reservation.objects.filter(user=request.user)
    return render(request, 'dashboard.html', {'borrowed_books': borrowed_books, 'reserved_books': reserved_books})

@login_required
def return_book(request, borrow_id):
    borrow = get_object_or_404(Borrow, id=borrow_id, user=request.user)
    if not borrow.returned:
        borrow.returned = True
        borrow.book.is_available = True  # make book available again
        borrow.book.save()
        borrow.save()
    return redirect('user_dashboard')

@login_required
def cancel_reservation(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id, user=request.user)
    reservation.delete()  # simply remove it
    return redirect('user_dashboard')

def logout_view(request):
    logout(request)
    return redirect('home')






