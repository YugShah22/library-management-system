from django.db import models
from django.contrib.auth.models import User
from datetime import date, timedelta

# Function to return default due date
def default_due_date():
    return date.today() + timedelta(days=14)

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    is_available = models.BooleanField(default=True)
    pages = models.PositiveBigIntegerField(blank=True, null=True)
    thumbnail = models.ImageField(
        upload_to='thumbnails/',
        blank=True,
        null=True,
        default='thumbnails/default.jpg'
    )

    def __str__(self):
        return self.title

class Borrow(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.PROTECT)
    borrow_date = models.DateField(default=date.today)
    due_date = models.DateField(default=default_due_date)
    returned = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} borrowed {self.book.title}"

class Reservation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.PROTECT)
    reserved_date = models.DateField(default=date.today)

    def __str__(self):
        return f"{self.user.username} reserved {self.book.title}"



