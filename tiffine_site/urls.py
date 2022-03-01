from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('menu/', MenuView.as_view(), name='menu'),
    path('order-deatial/<int:pk>', OrderPlace.as_view(), name='deatail-view'),
    path('payment-checkout/', PaymentCheckout.as_view(), name='payment-checkout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', login, name='login'),
    path('logout_user/', logout_user, name='logout_user'),
    path('add-favorite/', add_favorite, name='add-favorite'),
    path('user-profile/', user_profile, name='user-profile'),
    path('change-pass', change_passwd, name='change-pass'),

    path('password_reset/', auth_views.PasswordResetView.as_view(
        template_name='password_reset_form.html'
    ), name='password_reset'),

    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(
         template_name='password_reset_done.html'
         ), name='password_reset_done'),

    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        #     template_name='password_reset_confirm.html'
    ),
        name='password_reset_confirm'),

    path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(
         template_name='password_reset_complete.html'
         ),
         name='password_reset_complete'),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
