from django.urls import path

from .views import *

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('menu/', MenuView.as_view(), name = 'menu'),
    path('order-deatial/', OrderPlace.as_view(), name = 'deatail-view')
]