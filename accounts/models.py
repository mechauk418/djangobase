from re import T
from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class User(AbstractUser):
    email = models.EmailField(unique=True)
    last_login = None
    first_name = None
    last_name = None
    date_joined = None
    testtitle = models.CharField(blank=True, null=True, max_length=80)