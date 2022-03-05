from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.contrib.auth.models import AbstractUser

type_of = (
    ('veg', 'veg'),
    ('non_veg', 'non_veg'),
)


class MainDishModel(models.Model):
    name = models.CharField(max_length=100)
    deatil = models.CharField(max_length=255)
    price = models.FloatField()
    discounted = models.FloatField()
    availablity = models.BooleanField(default=True)
    image = models.ImageField(upload_to='pictures')
    ingredients = models.CharField(max_length=255)
    type_of = models.CharField(choices=type_of, max_length=10, blank=True)

    def __str__(self):
        return str(self.name)


class AddToFevorate(models.Model):
    user = models.ForeignKey(
        User, related_name='user_fevorate', on_delete=models.CASCADE)
    dish_name = models.ForeignKey(
        MainDishModel, related_name='dish_name', on_delete=models.CASCADE)
    is_fav = models.BooleanField(default=False)


class CommentAndRating(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    comment = models.TextField(max_length=250)
    rating = models.IntegerField(default=0)
    timestamp = models.DateTimeField(default=timezone.now)


class AddressModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    street = models.CharField(max_length=100, null=True)
    locality = models.CharField(max_length=100, null=True)
    landmark = models.CharField(max_length=100, null=True)
    city = models.CharField(max_length=100, null=True)
    pincode = models.IntegerField(null=True)


class PhoneNumber(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    number = models.IntegerField()
