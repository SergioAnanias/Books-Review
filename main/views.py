from django.shortcuts import render, HttpResponse, redirect
from .models import *
from django.contrib import messages
from django.db.models import Avg, Count
from django.http import JsonResponse
import bcrypt
from .decorators import loginauth

# Create your views here.
@loginauth
def index(request):

    context = {
        'books' : Book.objects.all().order_by('-id').annotate(Avg('reviews__rating')),
        'user' : User.objects.get(id=request.session['user']),
    }
    return render(request, "main.html", context)

def book(request, id):
    context = {
        'book': Book.objects.get(id=id)
    }
    return render(request, "book.html", context)

def user(request, id):
    context={
        'user': User.objects.get(id=id),
        'totalreviews': User.objects.aggregate(total_review=Count('reviews'))
    }
    return render(request, "user.html", context)

@loginauth
def addbook(request):
    context = {
        'authors': Author.objects.all()
    }
    return render(request, "addbook.html", context)

@loginauth
def newbook(request):
    if request.method == 'POST':
        # Validar
        # Validar si el autor elegido esta creado o no
        if len(Author.objects.filter(name=request.POST['newauthor'])) == 0 and request.POST['newauthor'] != '':
            newauthor = Author.objects.create(
                name= request.POST['newauthor']
                )
            newbook = Book.objects.create(
            title=request.POST['title'],
            author = newauthor
            )
        #Si esta creado do this:
        else:
            newbook = Book.objects.create(
                title=request.POST['title'],
                author = Author.objects.get(id=request.POST['author'])
            )
        newreview= Review.objects.create(
            review=request.POST['review'],
            rating=request.POST['rating'],
            user= User.objects.get(id=request.session['user']),
            book=newbook
        )
        return redirect(f'book/{newbook.id}')

@loginauth
def addreview(request):
    newreview = Review.objects.create(
        review=request.POST['review'],
        rating=request.POST['rating'],
        user= User.objects.get(id=request.session['user']),
        book= Book.objects.get(id=request.POST['book'])
    )
    return redirect(f'./{newreview.book.id}')

@loginauth
def deletereview(request):
    review = Review.objects.get(id=request.POST['review'])
    review.delete()
    return redirect('./'+request.POST['book'])