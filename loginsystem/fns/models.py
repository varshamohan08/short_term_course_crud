from django.db import models
from django.db.models.fields import TextField, EmailField
from django.db.models import JSONField
from django.contrib.auth.models import AbstractBaseUser

# Create your models here.
class user_data(AbstractBaseUser):
    first_name = TextField(blank= False, null= False)
    last_name = TextField()
    Email = EmailField(blank= False, null= False, unique=True)
    USERNAME_FIELD = 'Email'


class ShortTermCourse(models.Model):
    title = models.CharField(max_length=100)
    subtitle = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(default=None)
    amount = models.FloatField()
    additional_information = models.TextField()
    status = models.CharField(max_length=10, choices=[('Enable', 'Enable'), ('Disable', 'Disable')])
