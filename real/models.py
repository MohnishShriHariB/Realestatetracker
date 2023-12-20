from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Favorite(models.Model):
    type=models.CharField(max_length=255)
    county=models.CharField(max_length=255)
    address=models.CharField(max_length=255)
    price=models.CharField(max_length=255)
    status=models.CharField(max_length=255)
    size=models.CharField(max_length=255)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
