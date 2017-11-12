from __future__ import unicode_literals
from django.db import models
import re,  bcrypt
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')
class userManager(models.Manager):
    def add_user(self, postData):
        errors = []
        if User.objects.filter(email=postData['email']):
            errors.append("Email is already registered")
        if not EMAIL_REGEX.match(postData['email']):
            errors.append("Please enter a valid email!")
        if len(postData['password'])<8:
            errors.append("Password must contain at least 8 characters!")
        if(postData['password'] != postData['confirm']):
            errors.append("Passwords must match!")
        response = {}
        if errors:
            response['status'] = False
            response['error'] = errors
        else:
            errors.append('You registered succesfully!')
            response['status'] = True
            response['error'] = errors
            hashed = bcrypt.hashpw(postData['password'].encode(), bcrypt.gensalt())
            self.create(email=postData['email'], password=hashed)
        return response

    def login_user(self, postData):
        errors = []
        user = self.filter(email=postData['logEmail'])
        if not user:
            errors.append("Email  is not registered")
        elif not bcrypt.checkpw(postData['logPassword'].encode(), user[0].password.encode()):
                errors.append("Invalid Email Password combination")

        response = {}
        if errors:
            response['status'] = False
            response['error']= errors

        else:
            response['status']= True
            response['user']=user
        return response
class User(models.Model):
    email = models.CharField(max_length = 100)
    password = models.CharField(max_length =100)
    updated_at = models.DateTimeField(auto_now_add =True)
    created_at = models.DateTimeField(auto_now = True)
    objects = userManager()
