from tkinter.tix import Tree
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
import datetime
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
        User, related_name='user_fevorate', blank=True, null=True, on_delete=models.CASCADE)
    dish_name = models.ForeignKey(
        MainDishModel, related_name='dish_name', blank=True, null=True, on_delete=models.CASCADE)
    is_fav = models.BooleanField(default=False)


class CommentAndRating(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, blank=True, null=True, unique=False)
    dish = models.ForeignKey(
        MainDishModel, on_delete=models.SET_NULL, blank=True, null=True)
    comment = models.TextField(max_length=250)
    rating = models.IntegerField(default=0)
    timestamp = models.DateTimeField(auto_now_add=True)


class AddressModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    street = models.CharField(max_length=100, null=True)
    locality = models.CharField(max_length=100, null=True)
    landmark = models.CharField(max_length=100, null=True)
    city = models.CharField(max_length=100, null=True)
    phone = models.IntegerField(blank=True, null=True)
    pincode = models.IntegerField(null=True)


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(MainDishModel, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(blank=True, default=1)

    def amount_plus(self):
        return self.item.discounted * self.quantity

class OrderDetails(models.Model):
    user = models.ForeignKey(
        User, blank=True, null=True, on_delete=models.SET_NULL, editable=False)

    item_1 = models.ForeignKey(
        MainDishModel, blank=True, related_name='item_1', null=True, on_delete=models.SET_NULL, editable=False)
    qyt_1 = models.PositiveIntegerField(
        blank=True,  null=True, editable=False, )

    item_2 = models.ForeignKey(
        MainDishModel, blank=True, related_name='item_2', null=True, on_delete=models.SET_NULL, editable=False)
    qyt_2 = models.PositiveIntegerField(blank=True,  null=True, editable=False)

    item_3 = models.ForeignKey(
        MainDishModel, blank=True, related_name='item_3', null=True, on_delete=models.SET_NULL, editable=False)
    qyt_3 = models.PositiveIntegerField(
        blank=True, null=True, editable=False, )

    item_4 = models.ForeignKey(
        MainDishModel, blank=True, related_name='item_4', null=True, on_delete=models.SET_NULL, editable=False)
    qyt_4 = models.PositiveBigIntegerField(
        blank=True, null=True, editable=False, )

    item_5 = models.ForeignKey(
        MainDishModel, blank=True, related_name='item_5', null=True, on_delete=models.SET_NULL, editable=False)
    qyt_5 = models.PositiveBigIntegerField(
        blank=True, null=True, editable=False, )

    order_id = models.CharField(
        max_length=100, blank=True, null=True, editable=False)
    payment_id = models.CharField(
        max_length=100, blank=True, null=True, editable=False)
    date_time = models.DateTimeField(
        default=timezone.now, blank=True, null=True, editable=False)
    amount = models.FloatField(blank=True, null=True, editable=False)
    upi_transaction_id = models.CharField(
        max_length=100, blank=True, null=True, editable=False)
    vpa = models.CharField(max_length=100, blank=True,
                           null=True, editable=False)
    card_id = models.CharField(
        max_length=100, blank=True, null=True, editable=False)
    bank = models.CharField(max_length=100, blank=True,
                            null=True, editable=False)
    method = models.CharField(
        max_length=100, blank=True, null=True, editable=False)
    wallet = models.CharField(
        max_length=100, blank=True, null=True, editable=False)
