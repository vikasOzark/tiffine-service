from django.contrib import admin
from .models import MainDishModel, AddToFevorate

# Register your models here.


@admin.register(MainDishModel)
class AdminClass(admin.ModelAdmin):
    list_display = ['name', 'deatil', 'price',
                    'discounted', 'image', 'ingredients', 'availablity']


@admin.register(AddToFevorate)
class AdminClass(admin.ModelAdmin):
    list_display = ['user', 'dish_name']
