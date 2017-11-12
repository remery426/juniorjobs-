from __future__ import unicode_literals
from django.db import models
from ..login.models import User
import re,  bcrypt
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')

class searchManager(models.Manager):
    def addSearch(self, url, searchtext, currentUser):
        getUser = User.objects.filter(email = currentUser)
        print(getUser[0].id)
        search1 = self.create(searchText= searchtext,urlText=url)
        search1.userlist.add(getUser[0])
        return
class Search(models.Model):
    searchText = models.CharField(max_length = 100)
    urlText = models.CharField(max_length=1000)
    userlist = models.ManyToManyField(User, related_name = "userlist")
    updated_at = models.DateTimeField(auto_now_add =True)
    created_at = models.DateTimeField(auto_now = True)
    objects = searchManager()
