from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class TempestUser(User):
    #지역, 젠더, 연령
    age = models.CharField(max_length=10)
    region =  models.CharField(max_length=10)
    gender = models.CharField(max_length=10)