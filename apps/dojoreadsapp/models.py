from __future__ import unicode_literals
from django.db import models
import bcrypt

class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        # add keys and values to errors dictionary for each invalid field
        if len(postData['name']) < 5:
            errors["name"] = "Name should be at least 5 characters"
        if len(postData['email']) < 10:
            errors["email"] = "Email description should be at least 10 characters"
        if len(postData['password']) < 8:
            errors["password"] = "Password should be at least 8 characters"
        if postData['password'] != postData['confirm']:
            errors["email"] = "Passwords do not match"
        return errors
    def login_validator(self, postData):
        errors = {}
        user = User.objects.filter(email=postData['email']).values()
        print("***********", user)
        if len(postData['email']) < 10:
            errors["email"] = "Please enter email"
        if not user:
            errors["email"] = "Invalid email"
        else:
            if len(postData['password']) < 8:
                errors["password"] = "Please enter password"
            elif bcrypt.checkpw(postData['password'].encode(), user[0]['password'].encode()):
                pass
            else:
                errors["password"] = "Invalid password"
        return errors

class User(models.Model):
    name = models.CharField(max_length=45)
    email = models.CharField(max_length=45)
    password = models.CharField(max_length=45)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Book(models.Model):
    title = models.CharField(max_length=45)
    author = models.CharField(max_length=45)
    added_by = models.ForeignKey(User, related_name="books")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Review(models.Model):
    content = models.TextField()
    rating = models.IntegerField()
    reviewer = models.ForeignKey(User, related_name="user_reviews")
    book = models.ForeignKey(Book, related_name="book_reviews")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)