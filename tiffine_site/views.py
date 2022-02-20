from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import View
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.decorators import login_required


# Create your views here.


class IndexView(View):
    def get(self, request, *args, **kwargs):
        return render(request, template_name='index.html')


class MenuView(View):
    def get(self, request, *args, **kwargs):
        return render(request, template_name='menu.html')


class OrderPlace(View):
    def get(self, request, *args, **kwargs):
        return render(request, template_name='deatail_view.html')


class PaymentCheckout(View):
    def get(self, request):
        return render(request, template_name='payment_checkout.html')


class RegisterView(View):
    def post(self, request):
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')

        if password == password2:
            user = User.objects.create_user(
                first_name=first_name,
                last_name=last_name,
                username=username,
                email=email,
                password=password,
            )

            user.save()

            user = authenticate(request, username=username, password=password)
            if user is not None:
                print('yess')
                auth_login(request, user)
                messages.success(request, f"{user.username}, You successfully registered !",
                                 extra_tags='alert-success')
                return redirect("index")

            else:
                messages.warning(request, 'Something is wrong !')

        return render(request, template_name='register.html')


def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        passwd = request.POST.get('password')

        user = authenticate(request, username=username, password=passwd)
        if user is not None:
            auth_login(request, user)

            messages.success(
                request, f'{user.username} ,You loged in successfully!', extra_tags='alert-success shadow')
            return redirect('index')

        else:
            messages.warning(request, 'Something is wrong !.',
                             extra_tags='alert-warning shadow')
            return redirect('login')

    return render(request, template_name='login.html')


def logout_user(request):
    logout(request)

    return redirect('index')
