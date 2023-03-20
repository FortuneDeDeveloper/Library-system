from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse 
import uuid
from datetime import date

# Create your models here

class UserData(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    student_number = models.IntegerField()

class Genre(models.Model):
    name = models.CharField(max_length=200, help_text="Enter a book genre")
    
    
    def __str__(self):
        """String representing the Model project"""
        return self.name
    
class Book(models.Model):
    title = models.CharField(max_length=200)
    cover = models.ImageField(upload_to = 'pics')
    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)
    content = models.FileField(upload_to='pdfs',null=True,verbose_name=" ")
    genre = models.ManyToManyField('Genre', help_text='Select a genre for this book')
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('book-detail', args=[str(self.id)])
    
class BookInstance(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='unique id for this book')
    book = models.ForeignKey('Book', on_delete=models.RESTRICT, null=True)
    due_back = models.DateField(null=True, blank=True)
    borrower = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def is_overdue(self):
        """Determines if the book is overdue based on due date and current date."""
        return bool(self.due_back and date.today() > self.due_back)

    
    LOAN_STATUS = (
    ('o', 'on loan'),
    ('a', 'Available'),
)
    status = models.CharField(
    max_length=1,
    choices = LOAN_STATUS,
    blank=True,
    default='a',
    help_text='Book availability',
)

    class Meta:
        ordering = ['due_back']
    

    def __str__(self):
        return f'{self.id} ({self.book.title})'


class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    
    class Meta:
        ordering = ['last_name', 'first_name']
        permissions = (("can_mark_returned", "Set book as returned"),)
    
    def get_absolute_url(self):
        return reverse("author-detail", arg=[str(self.id)])

    def __str__(self):
        return f'{self.last_name}, {self.first_name}'

# def display_genre(self):
#     return ', '.join(genre.name for genre in self.genre.all()[:3])

# display_genre.short_description = 'Genre'
