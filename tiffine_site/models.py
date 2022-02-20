from django.db import models
from django.contrib.auth.models import User
from matplotlib.style import available


class MainDishModel(models.Model):
    name = models.CharField(max_length=100)
    deatil = models.CharField(max_length=255)
    price = models.FloatField()
    discounted = models.FloatField()
    availablity = models.BooleanField(default=True)
    image = models.ImageField(upload_to='pictures')
    ingredients = models.CharField(max_length=255)


class AddToFevorate(models.Model):
    user = models.ForeignKey(
        User, related_name='user_fevorate', on_delete=models.CASCADE)
    dish_name = models.ForeignKey(
        MainDishModel, related_name='dish_name', on_delete=models.CASCADE)
