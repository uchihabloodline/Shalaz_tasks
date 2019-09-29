#from django.db import models
#import urllib2
#import mimetypes

from django.conf import settings
from django.db import models
#from django.contrib.auth.models import User

# Create your models here.

class User(models.Model):
    username = models.CharField(max_length = 100,unique=True,verbose_name="username")
    password = models.CharField(max_length = 100)


class Post(models.Model):
	author = models.CharField(max_length = 100)
	title = models.CharField(max_length = 100,unique=True)
	content = models.TextField()
	created_on = models.DateField(auto_now_add=True)
	#publish_on = models.DateField()

class Restaurent(models.Model):
	res_id = models.IntegerField(verbose_name="res_id", unique=True)
	details = models.TextField(verbose_name="Json Data")

class Favourite(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, to_field="username")
	restaurent = models.ForeignKey(Restaurent, on_delete=models.CASCADE, to_field="res_id")

class Booking(models.Model):
	restaurent = models.ForeignKey(Restaurent, on_delete=models.CASCADE, to_field="res_id")
	time = models.TimeField()
	guests = models.IntegerField(verbose_name="guests", name="guests", default=1)