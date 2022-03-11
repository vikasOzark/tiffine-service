from django.contrib import admin
from .models import MainDishModel, AddToFevorate, CommentAndRating, AddressModel, PhoneNumber, OrderDetails, Cart

# Register your models here.


@admin.register(MainDishModel)
class Dishes(admin.ModelAdmin):
    list_display = ['id', 'name', 'deatil', 'price',
                    'discounted', 'image', 'ingredients', 'type_of', 'availablity']


@admin.register(AddToFevorate)
class Fvorite(admin.ModelAdmin):
    list_display = ['id', 'user', 'dish_name']


@admin.register(CommentAndRating)
class Ratings(admin.ModelAdmin):
    list_display = ['id', 'user', 'dish', 'comment', 'rating', 'timestamp']


@admin.register(AddressModel)
class UserAddress(admin.ModelAdmin):
    list_display = ['id', 'user', 'street',
                    'locality', 'landmark', 'city', 'pincode']


@admin.register(PhoneNumber)
class Numbers(admin.ModelAdmin):
    list_display = ['id', 'user', 'number']


@admin.register(OrderDetails)
class OrderDetail(admin.ModelAdmin):
    list_display = ['id', 'user', 'order_id', 'items', 'date_time', 'amount']


@admin.register(Cart)
class OrderDetail(admin.ModelAdmin):
    list_display = ['id', 'user', 'item']
