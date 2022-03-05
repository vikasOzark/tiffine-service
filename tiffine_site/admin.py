from django.contrib import admin
from .models import MainDishModel, AddToFevorate, CommentAndRating, AddressModel, PhoneNumber

# Register your models here.


@admin.register(MainDishModel)
class AdminClass(admin.ModelAdmin):
    list_display = ['id', 'name', 'deatil', 'price',
                    'discounted', 'image', 'ingredients', 'type_of', 'availablity']


@admin.register(AddToFevorate)
class AdminClass(admin.ModelAdmin):
    list_display = ['id', 'user', 'dish_name']


@admin.register(CommentAndRating)
class AdminClass(admin.ModelAdmin):
    list_display = ['id', 'user', 'comment', 'rating', 'timestamp']


@admin.register(AddressModel)
class AdminClass(admin.ModelAdmin):
    list_display = ['id', 'user', 'street',
                    'locality', 'landmark', 'city', 'pincode']


@admin.register(PhoneNumber)
class AdminClass(admin.ModelAdmin):
    list_display = ['id', 'user', 'number']
