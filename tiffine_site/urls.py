from django.urls import path

from .views import *

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('menu/', MenuView.as_view(), name = 'menu'),
    path('order-deatial/', OrderPlace.as_view(), name = 'deatail-view'),
    path('payment-checkout/', PaymentCheckout.as_view(), name = 'payment-checkout'),
    path('register/', RegisterView.as_view(), name = 'register'),
    path('login/', login, name = 'login'),
    path('logout_user/', logout_user , name = 'logout_user')
]
