from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('menu/', MenuView.as_view(), name='menu'),
    path('order-deatial/', OrderPlace.as_view(), name='deatail-view'),
    path('payment-checkout/', PaymentCheckout.as_view(), name='payment-checkout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', login, name='login'),
    path('logout_user/', logout_user, name='logout_user'),
    path('add-favorite/', add_favorite, name='add-favorite')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
