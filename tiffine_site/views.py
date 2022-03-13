from xml.etree.ElementTree import Comment
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.views import View
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.decorators import login_required
from secretstorage import Item
from .models import MainDishModel, AddToFevorate, AddressModel, PhoneNumber, CommentAndRating, Cart
from django.db.models import Q
from django.core import serializers
from .forms import AddressForm

# Create your views here.


class IndexView(View):
    def get(self, request, *args, **kwargs):
        return render(request, template_name='index.html')


class MenuView(View):
    def get(self, request, slug=None, *args, **kwargs):
        favorite = AddToFevorate.objects.filter(user=request.user)
        is_cart = Cart.objects.filter(user=request.user)

        if slug == 'veg':
            menu_model = MainDishModel.objects.filter(type_of='veg')
        elif slug == 'non_veg':
            menu_model = MainDishModel.objects.filter(type_of='non_veg')
        elif slug == 'all':
            menu_model = MainDishModel.objects.all()
        else:
            menu_model = MainDishModel.objects.all()

        template = 'menu.html'

        context = {
            'menu_model': menu_model,
            'fav': favorite,
            'is_cart': is_cart

        }
        return render(request, template_name=template, context=context)


class OrderPlace(View):
    def get(self, request, *args, **kwargs):
        dish_obj = MainDishModel.objects.get(pk=kwargs['pk'])
        favorite = AddToFevorate.objects.filter(user=request.user)
        rating_obj = CommentAndRating.objects.filter(pk=kwargs['pk'])
        # rating_obj = CommentAndRating.objects.all()

        is_cart = Cart.objects.filter(user=request.user)

        is_c = Cart.objects.filter(
            Q(user=request.user) & Q(item=dish_obj)).exists()

        print('=====> ', is_c)
        is_favorite = AddToFevorate.objects.filter(
            Q(user=request.user) & Q(dish_name=kwargs['pk'])).exists()
        context = {
            'dish_obj': dish_obj,
            'fav': favorite,
            'is_favorite': is_favorite,
            'rating_obj': rating_obj,
            'is_cart': is_cart,
            'is_c': is_c
        }
        template = 'deatail_view.html'
        return render(request, template_name=template, context=context)


class PaymentCheckout(View):
    def get(self, request, *args, **kwargs):

        cart_instance = Cart.objects.filter(user=request.user)

        template = 'payment_checkout.html'
        context = {
            'dish_instance': cart_instance
        }

        return render(request, template_name=template, context=context)


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

        is_favorite = AddToFevorate.objects.filter(
            Q(user=request.user) & Q(dish_name=dish_obj)).exists()
        if is_favorite == False:
            save_fav = AddToFevorate(user=request.user, dish_name=dish_obj)
            save_fav.save()
            return JsonResponse({'status': 'Save', 'data_coming': 'red'})
        else:
            favorite = AddToFevorate.objects.get(
                Q(user=request.user) and Q(dish_name=dish_obj))
            favorite.delete()
            return JsonResponse({'status': 'Deleted', 'data_coming': 'black'})


@ login_required(login_url='login')
def user_profile(request):
    address = AddressModel.objects.filter(user=request.user)
    phone = PhoneNumber.objects.filter(user=request.user)

    context = {
        'address': address,
        'phone': phone,
        'add_form': AddressForm
    }
    template = 'profile.html'
    return render(request, template_name=template, context=context)


def change_passwd(request):
    if request.method == "POST":

        password = request.POST.get('password')
        new_passwd = request.POST.get('new_passwd')
        new_passwd2 = request.POST.get('new_passwd2')

        if new_passwd == new_passwd2:
            user = authenticate(
                request, username=request.user, password=password)

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


def sav_address(request):
    if request.method == 'POST':
        form = AddressForm(request.POST)
        if form.is_valid():
            street = request.POST['street']
            locality = request.POST['locality']
            landmark = request.POST['landmark']
            city = request.POST['city']
            pincode = request.POST['pincode']
            id = request.POST.get('id')

            if id == '':
                address_obj = AddressModel(
                    user=request.user,
                    street=street,
                    locality=locality,
                    landmark=landmark,
                    city=city,
                    pincode=pincode,
                )
            else:
                address_obj = AddressModel(
                    user=request.user,
                    id=id,
                    street=street,
                    locality=locality,
                    landmark=landmark,
                    city=city,
                    pincode=pincode,
                )
            address_obj.save()

            data_obj = AddressModel.objects.values()
            data_obj = list(data_obj)

            messages.success(request, 'Successfully saved address !')
            return JsonResponse({'status': 'saved', 'data_obj': data_obj})
        else:
            messages.info(request, 'Address not saved !')
            return JsonResponse({'status': 'Wrong', 'data_obj': data_obj})


def delete_address(request):
    if request.method == "POST":
        id = request.POST.get('sid')
        addr_obj = AddressModel.objects.get(pk=id)
        addr_obj.delete()
        return JsonResponse({'status': '200'})
    else:
        return JsonResponse({'status': '420'})


def edit_address(request):
    if request.method == 'POST':
        id = request.POST.get('sid')
        addr_obj = AddressModel.objects.get(pk=id)
        addr_data = {
            'street': addr_obj.street,
            'landmark': addr_obj.landmark,
            'city': addr_obj.city,
            'locality': addr_obj.locality,
            'pincode': addr_obj.pincode,
            'id': addr_obj.id
        }
        return JsonResponse(addr_data)


def ratings(request):
    if request.method == 'GET':
        comment = request.GET.get('comment')
        rating = request.GET.get('userRating')
        id = request.GET.get('id')
        dish_obj = MainDishModel.objects.get(pk=id)

        model_ins = CommentAndRating(
            user=request.user,
            dish=dish_obj,
            comment=comment,
            rating=rating
        )

        model_ins.save()
        model_obj = CommentAndRating.objects.values()
        model_obj = list(model_obj)
        return JsonResponse({'status': '200', 'objects': model_obj})


def AddToDabba(request):
    if request.method == 'GET':
        id_ = request.GET.get('dish_id')
        item_obj = MainDishModel.objects.get(pk=id_)
        is_cart = Cart.objects.filter(
            Q(user=request.user) & Q(item=item_obj)).exists()

        if is_cart == True:
            obj = Cart.objects.get(Q(user=request.user) & Q(item=item_obj))
            obj.delete()
            return JsonResponse({'status': 'delete', 'is_cart': 'Add cart'})

        else:
            cart_instance = Cart(
                user=request.user,
                item=item_obj
            )

            cart_instance.save()

            return JsonResponse({'status': 'save', 'is_cart': 'Added'})

    if request.method == 'POST':
        id_ = request.POST.get('dish_id')
        try:
            get_obj = Cart.objects.get(Q(pk=id_) & Q(user=request.user))
            get_obj.delete()

            return JsonResponse({'status': 'delete'})
        except:
            print('not working')
            return JsonResponse({'status': '400'})


def adding_quantity(request):
    if request.method == 'GET':
        item_id = request.GET.get('item_id')
        qty_val = request.GET.get('quantity')

        item_id = int(item_id)
        qty_val = int(qty_val)

        cart_obj = Cart.objects.get(
            id=item_id,
        )
        cart_obj.quantity = qty_val
        cart_obj.save()

        return JsonResponse({'status': 'Updated'})
