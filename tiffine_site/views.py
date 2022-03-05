from ast import Add
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.views import View
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.decorators import login_required
from .models import MainDishModel, AddToFevorate, AddressModel, PhoneNumber
from django.db.models import Q
import json
from django.core import serializers

# Create your views here.


class IndexView(View):
    def get(self, request, *args, **kwargs):
        return render(request, template_name='index.html')


class MenuView(View):
    def get(self, request, slug=None, *args, **kwargs):
        print(slug)
        favorite = AddToFevorate.objects.filter(user=request.user)

        if slug == 'veg':
            menu_model = MainDishModel.objects.filter(type_of='veg')
        elif slug == 'non_veg':
            menu_model = MainDishModel.objects.filter(type_of='non_veg')
        elif slug == 'all':
            menu_model = MainDishModel.objects.all()
        else:
            menu_model = MainDishModel.objects.all()

        template = 'menu.html'
        print(favorite)

        context = {
            'menu_model': menu_model,
            'fav': favorite
        }
        return render(request, template_name=template, context=context)


class OrderPlace(View):
    def get(self, request, *args, **kwargs):
        dish_obj = MainDishModel.objects.get(pk=kwargs['pk'])
        context = {
            'dish_obj': dish_obj
        }
        template = 'deatail_view.html'
        return render(request, template_name=template, context=context)


class PaymentCheckout(View):
    def get(self, request):
        return render(request, template_name='payment_checkout.html')


class RegisterView(View):
    def get(self, request):
        return render(request, template_name='register.html')

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
                request, f'{user.username} ,You loged in successfully!', extra_tags='alert-success shadow border')
            return redirect('index')

        else:
            messages.warning(request, 'Something is wrong !.',
                             extra_tags='alert-warning shadow border')
            return redirect('login')

    return render(request, template_name='login.html')


def logout_user(request):
    logout(request)
    return redirect('index')


def add_favorite(request):
    if request.method == "GET":
        prod_id = request.GET.get('item_id')
        dish_obj = MainDishModel.objects.get(id=prod_id)
        print(dish_obj)
        is_favorite = AddToFevorate.objects.filter(
            Q(user=request.user) & Q(dish_name=dish_obj)).exists()
        print(is_favorite)
        if is_favorite == False:
            save_fav = AddToFevorate(user=request.user, dish_name=dish_obj)
            save_fav.save()
            return JsonResponse({'status': 'Save', 'data_coming': 'red'})
        else:
            favorite = AddToFevorate.objects.get(
                Q(user=request.user) and Q(dish_name=dish_obj))
            favorite.delete()
            return JsonResponse({'status': 'Deleted', 'data_coming': 'black'})


@login_required(login_url='login')
def user_profile(request):
    address = AddressModel.objects.filter(user = request.user)
    phone = PhoneNumber.objects.filter(user = request.user)

    context = {
        'address' : address,
        'phone' : phone
    }
    template = 'profile.html'
    return render(request, template_name=template, context = context)


def change_passwd(request):
    if request.method == "POST":

        password = request.POST.get('password')
        new_passwd = request.POST.get('new_passwd')
        new_passwd2 = request.POST.get('new_passwd2')

        if new_passwd == new_passwd2:
            user = authenticate(
                request, username=request.user, password=password)
            print(user)

            if user is not None:
                passwd = User.objects.get(username=request.user)
                passwd.set_password(new_passwd)
                passwd.save()
                logout(request)

                message = messages.info(
                    request, 'Congrats, You have successfully changed your password !')
                try:
                    return redirect('login')
                except:
                    return JsonResponse({'status': 'done'})
            else:
                message = messages.warning(
                    request, 'Your old password is wrong !', extra_tags='')
                return JsonResponse({'status': 'old passwor wrong'})
        else:
            message = messages.info(request, 'Password supposed to be same  !')
            return JsonResponse({'status': 'not matched'})


def filter_menu(request):
    if request.method == 'GET':
        type_of = request.GET.get('type_val')
        print(type_of)
        if type_of == 'non_veg':
            data = serializers.serialize(
                "json", MainDishModel.objects.filter(type_of=type_of), fields=(
                    'name', 'deatil', 'price', 'discounted', 'availablity', 'image', 'ingredients', 'type_of'))
            return JsonResponse({'status': 'working', 'datas': data})
        if type_of == 'veg':
            data = serializers.serialize(
                "json", MainDishModel.objects.filter(type_of=type_of), fields=(
                    'name', 'deatil', 'price', 'discounted', 'availablity', 'image', 'ingredients', 'type_of'))
            return JsonResponse({'status': 'working', 'datas': data})
