from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
import bcrypt
def index(request):
    if 'name' in request.session:
        del request.session['name']
    return render(request, "dojoreadsapp/index.html")
def readall(request):
    if 'name' not in request.session:
        return redirect('/')
    else:
        context = {
            "last_three_reviews": Review.objects.order_by("-created_at")[:3],
            "books": Book.objects.all()
        }
        return render(request, "dojoreadsapp/books.html", context)
def add(request):
    context = {
        "books": Book.objects.all()
    }
    return render(request, "dojoreadsapp/addbook.html", context)
def readone(request, id):
    x = Book.objects.get(id=id)
    context = {
        "book": x,
    }
    return render(request, "dojoreadsapp/bookid.html", context)
def readuser(request, id):
    user = User.objects.get(id=id)
    context = {
        "user": user,
        "books": Review.objects.filter(reviewer=user)
    }
    return render(request, "dojoreadsapp/user.html", context)
def register(request):
    errors = User.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        if request.method == "POST":
            name = request.POST['name']
            request.session['name'] = request.POST['name']
            email = request.POST['email']
            password = request.POST['password']
            hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
            User.objects.create(name=name, email=email, password=hash)
            return redirect('/books')
def login(request):
    errors = User.objects.login_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    if request.method == "POST":
        user = User.objects.filter(email = request.POST['email']).values()
        request.session['name'] = user[0]['name']
        return redirect("/books")
def create_book(request):
    if request.method == "POST":
        title = request.POST['title']
        author = request.POST['author']
        user = User.objects.get(name = request.session['name'])
        Book.objects.create(title=title, author=author, added_by=user)
        content = request.POST['content']
        rating = request.POST['rating']
        print("*************", rating)
        book = Book.objects.last()
        Review.objects.create(content=content, rating=rating, reviewer=user, book=book)
        id = str(book.id)
        return redirect("/books/" + id)
def addreview(request, id):
    if request.method == "POST":
        book = Book.objects.get(id=id)
        user = User.objects.get(name = request.session['name'])
        content = request.POST['content']
        rating = request.POST['rating']
        Review.objects.create(content=content, rating=rating, reviewer=user, book=book)
        return redirect("/books/" + id)
