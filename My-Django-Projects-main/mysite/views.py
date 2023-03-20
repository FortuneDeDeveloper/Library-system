from multiprocessing import context
from urllib import request
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from .decorators import unauthenticated_user
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin

from mysite.models import UserData, Book, Author, BookInstance
from .forms import NewUserForm, Borrowed_books
from django.contrib import messages
from django.contrib.auth import authenticate,login
from django.contrib.auth.decorators import login_required
from .models import BookInstance

# Create your views here.

@unauthenticated_user
def register(request):
    form = NewUserForm()

    if request.method == 'POST':
        form = NewUserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            student_number = form.cleaned_data.get('student_number')
            user = User.objects.get(username=username)
            user_data = UserData.objects.create(user=user, student_number=student_number)
            user_data.save()
            messages.success(request,"Account was created successfully for "+ username)
            return redirect('login')
    context = {'form':form}
    return render(request,'signup_signin.html',context)

@unauthenticated_user
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,"Username OR Password incorrect")
    context = {}
    return render(request,'login.html',context)

@login_required(login_url='login')
def index(request):
    books = Book.objects.all()
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()
    
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()
    
    num_authors = Author.objects.count()
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1
    
    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_visits': num_visits,
        'Books':books,
    }
    return render(request,'index.html',context)

@login_required(login_url='login')
def error(request):
    return render(request,'404.html')

@login_required(login_url='login')
def aboutUs(request):
    return render(request,'aboutus.html')

@login_required(login_url='login')
def results(request):
    if request.method == 'POST':
        searched = request.POST['searched']
        books = Book.objects.filter(title__icontains = searched)
        if books.exists():
            context = {'searched':searched,'books':books}
            return render(request,'searched.html',context)
        else:
            return redirect('error')
    else:
        context = {}
        return render(request,'searched.html',context)

@login_required(login_url='login')
def base_template(request):
    return render(request,'base.html')

@login_required(login_url='login')
def shelf(request):
    books = BookInstance.objects.all()
    num_instances = BookInstance.objects.all().count()
    context = {
        'Bookinstance_list':books,
        'num_borrowed_books': num_instances,
    }
    return render(request,'shelf.html',context)

@login_required(login_url='login')
def borrow_book(request):
    form = Borrowed_books()

    if request.method == 'POST':
        form = Borrowed_books(request.POST)
        book_being_borrowed = request.POST['book']
        if BookInstance.objects.filter(book=book_being_borrowed).exists():
            messages.error(request,'The book is on loan')
            return redirect('borrow-book')
        else:
            if form.is_valid():
                book_instance = form.save(commit=False)
                book_instance.status = 'o'
                book_instance.save()
                messages.success(request,"You have successfully borrowed the book")
                return redirect('shelf')
            else:
                messages.error(request,'The information provided is not valid')
                return redirect('borrow-book')
    context={'form':form}
    return render(request,'borrow_book.html',context)
            
class BookListView(generic.ListView):
    model = Book
    paginate_by = 2
    
class BookDetailView(generic.DetailView):
    model = Book
    

class LoanedBooksByUserListView(LoginRequiredMixin,generic.ListView):
    """Generic class-based view listing books on loan to current user."""
    model = BookInstance
    template_name ='catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')
        
