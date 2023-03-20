from django.conf import settings
from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

#The url mappings go here

urlpatterns = [
    path('',views.register,name='register'),
    path('login/',views.user_login,name='login'),
    path('home/',views.index,name='home'),
    path('404/',views.error,name='error'),
    path('aboutus/',views.aboutUs,name='aboutUs'),
    path('searched/',views.results,name='searched'),
    path('logout/', LogoutView.as_view(next_page=settings.LOGOUT_REDIRECT_URL), name='logout'),
    path('books/', views.BookListView.as_view(), name='books'),
    path('book/<int:pk>', views.BookDetailView.as_view(), name='book-detail'),
    path('base/',views.base_template,name='base'),
    path('borrow/',views.borrow_book,name='borrow-book'),
    path('shelf/',views.shelf,name='shelf'),
]

urlpatterns += [
    path('mybooks/', views.LoanedBooksByUserListView.as_view(), name='my-borrowed'),
]
