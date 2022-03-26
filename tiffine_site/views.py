from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.views import View
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.decorators import login_required
from .models import MainDishModel, AddToFevorate, AddressModel, CommentAndRating, Cart, OrderDetails
from django.db.models import Q
from django.core import serializers
from .forms import AddressForm
from django.views.decorators.csrf import csrf_exempt
import razorpay
from django.conf import settings

# Create your views here.

# RAZOR_KEY_ID = 'rzp_test_HwKecOzHzISyXr'
# RAZOR_KEY_SECRET = 'bDcjVc789fO9Prz8kCDgm2yP'


class IndexView(View):
    def get(self, request, *args, **kwargs):
        return render(request, template_name='index.html')


class MenuView(View):
    def get(self, request, slug=None, *args, **kwargs):

        if request.user.is_authenticated:
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
        else:

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
            }
            return render(request, template_name=template, context=context)


class OrderPlace(View):
    def get(self, request, *args, **kwargs):

        dish_obj = MainDishModel.objects.get(pk=kwargs['pk'])
        rating_obj = CommentAndRating.objects.filter(pk=kwargs['pk'])

        if request.user.is_authenticated:
            favorite = AddToFevorate.objects.filter(user=request.user)
            is_cart = Cart.objects.filter(user=request.user)
            is_c = Cart.objects.filter(
                Q(user=request.user) & Q(item=dish_obj)).exists()
            is_favorite = AddToFevorate.objects.filter(
                Q(user=request.user) & Q(dish_name=kwargs['pk'])).exists()

            context = {
                'fav': favorite,
                'is_favorite': is_favorite,
                'rating_obj': rating_obj,
                'is_cart': is_cart,
                'is_c': is_c,
                'dish_obj': dish_obj,
                'rating_obj': rating_obj,
            }

        context = {
            'dish_obj': dish_obj,
            'rating_obj': rating_obj,
        }
        template = 'deatail_view.html'
        return render(request, template_name=template, context=context)


razorpay_client = razorpay.Client(
    auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))


class PaymentCheckout(View):
    razorpay_client = razorpay.Client(
        auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))

    def get(self, request, *args, **kwargs):
        cart_instance = Cart.objects.filter(user=request.user)

        final_amount = 0
        for obj in cart_instance:
            qyt_ins = obj.quantity
            amount_ins = obj.item.discounted
            final_amount += amount_ins * qyt_ins

        currency = 'INR'
        amount = (final_amount + 50) * 100

        plus_delivery = final_amount + 50
        # Create a Razorpay Order
        razorpay_order = razorpay_client.order.create(dict(amount=amount,
                                                           currency=currency,
                                                           payment_capture='0'))

        # order id of newly created order.
        razorpay_order_id = razorpay_order['id']
        # callback_url = 'paymenthandler'

        template = 'payment_checkout.html'
        context = {
            'dish_instance': cart_instance,
            'razorpay_order_id': razorpay_order_id,
            'razorpay_merchant_key': 'rzp_test_CACIK9VunIicKe',
            'razorpay_amount': amount,
            'currency': currency,
            # 'callback_url': callback_url
            'final_amount': final_amount,
            'plus_delivery': plus_delivery,

        }

        return render(request, template_name=template, context=context)


@csrf_exempt
def paymenthandler(request):

    # only accept POST request.
    if request.method == "POST":
        try:

            # get the required parameters from post request.
            payment_id = request.POST.get('razorpay_payment_id', '')
            razorpay_order_id = request.POST.get('razorpay_order_id', '')
            signature = request.POST.get('razorpay_signature', '')

            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            }

            cart_items = Cart.objects.filter(user=request.user)

            result = razorpay_client.utility.verify_payment_signature(
                params_dict)

            final_amount = 0
            for obj in cart_items:
                qyt_ins = obj.quantity
                amount_ins = obj.item.discounted
                final_amount += amount_ins * qyt_ins

            if result is True:
                amount = (final_amount + 50) * 100  # Rs. 200
                try:
                    # capture the payemt
                    data = razorpay_client.payment.capture(payment_id, amount)

                    item_obj = []
                    qyt_obj = []
                    for cart_obj in cart_items:
                        x = MainDishModel.objects.get(pk=cart_obj.item.id)
                        item_obj.append(x)
                        qyt_obj.append(cart_obj.quantity)

                    if len(item_obj) == 1:
                        obj = OrderDetails(
                            user=request.user,
                            item_1=item_obj[0],
                            qyt_1=qyt_obj[0],

                            order_id=data['order_id'],
                            amount=data['amount'],
                            payment_id=data['id'],
                            vpa=data['vpa'],
                            upi_transaction_id=data['acquirer_data']['upi_transaction_id'],
                            method=data['method'],
                            wallet=['wallet'],
                            card_id=data['card_id'],
                            bank=data['bank']
                        )
                        obj.save()

                    if len(item_obj) == 2:
                        obj = OrderDetails(
                            user=request.user,
                            item_1=item_obj[0],
                            qyt_1=qyt_obj[0],
                            item_2=item_obj[1],
                            qyt_2=qyt_obj[1],

                            order_id=data['order_id'],
                            amount=data['amount'],
                            payment_id=data['id'],
                            vpa=data['vpa'],
                            upi_transaction_id=data['acquirer_data']['upi_transaction_id'],
                            method=data['method'],
                            wallet=['wallet'],
                            card_id=data['card_id'],
                            bank=data['bank']
                        )
                        obj.save()

                    if len(item_obj) == 3:
                        obj = OrderDetails(
                            user=request.user,
                            item_1=item_obj[0],
                            qyt_1=qyt_obj[0],
                            item_2=item_obj[1],
                            qyt_2=qyt_obj[1],
                            item_3=item_obj[2],
                            qyt_3=qyt_obj[2],

                            order_id=data['order_id'],
                            amount=data['amount'],
                            payment_id=data['id'],
                            vpa=data['vpa'],
                            upi_transaction_id=data['acquirer_data']['upi_transaction_id'],
                            method=data['method'],
                            wallet=['wallet'],
                            card_id=data['card_id'],
                            bank=data['bank']
                        )
                        obj.save()

                    if len(item_obj) == 4:
                        obj = OrderDetails(
                            user=request.user,
                            item_1=item_obj[0],
                            qyt_1=qyt_obj[0],
                            item_2=item_obj[1],
                            qyt_2=qyt_obj[1],
                            item_3=item_obj[2],
                            qyt_3=qyt_obj[2],
                            item_4=item_obj[3],
                            qyt_4=qyt_obj[3],

                            order_id=data['order_id'],
                            amount=data['amount'],
                            payment_id=data['id'],
                            vpa=data['vpa'],
                            upi_transaction_id=data['acquirer_data']['upi_transaction_id'],
                            method=data['method'],
                            wallet=['wallet'],
                            card_id=data['card_id'],
                            bank=data['bank']
                        )
                        obj.save()

                    if len(item_obj) == 5:
                        obj = OrderDetails(
                            user=request.user,
                            item_1=item_obj[0],
                            qyt_1=qyt_obj[0],
                            item_2=item_obj[1],
                            qyt_2=qyt_obj[1],
                            item_3=item_obj[2],
                            qyt_3=qyt_obj[2],
                            item_4=item_obj[3],
                            qyt_4=qyt_obj[3],
                            item_5=item_obj[4],
                            qyt_5=qyt_obj[4],

                            order_id=data['order_id'],
                            amount=data['amount'],
                            payment_id=data['id'],
                            vpa=data['vpa'],
                            upi_transaction_id=data['acquirer_data']['upi_transaction_id'],
                            method=data['method'],
                            wallet=['wallet'],
                            card_id=data['card_id'],
                            bank=data['bank']
                        )
                        obj.save()

                    cart_del = Cart.objects.filter(user=request.user)
                    cart_del.delete()
                    return render(request, 'index.html')
                    # render success page on successful caputre of payment

                except Exception as e:

                    # if there is an error while capturing payment.
                    print('====> if not captured : ', e)

                    return render(request, 'faild.html')
            else:

                # if signature verification fails.
                print('====> if resut false : ')

                return render(request, 'faild.html')
        except:

            # if we don't find the required parameters in POST data
            print('====> if  if we don t find the required parameters in POST data : ')

            return HttpResponseBadRequest()
    else:
       # if other than POST request is made.
        return HttpResponseBadRequest()


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


@login_required(login_url='login')
def user_profile(request):
    address = AddressModel.objects.filter(user=request.user)
    orders = OrderDetails.objects.filter(user=request.user)
    phones = AddressModel.objects.filter(user=request.user)
    try:
        phone = []
        for i in phones:
            phone.append(i.phone)
        context = {
            'address': address,
            'add_form': AddressForm,
            'orders': orders,
            'phone': phone[0]
        }
        template = 'profile.html'
        return render(request, template_name=template, context=context)

    except:
        phone = ['Please add number while adding address !']

        context = {
            'address': address,
            'add_form': AddressForm,
            'orders': orders,
            'phone': phone[0]
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
            phone = request.POST['phone']
            pincode = request.POST['pincode']
            id = request.POST.get('id')

            if id == '':
                address_obj = AddressModel(
                    user=request.user,
                    street=street,
                    locality=locality,
                    landmark=landmark,
                    city=city,
                    phone=phone,
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
                    phone=phone,
                    pincode=pincode,
                )
            address_obj.save()

            data_obj = AddressModel.objects.values()
            data_obj = list(data_obj)

            messages.success(request, 'Address saved successfully  !', extra_tags='')
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
            'phone': addr_obj.phone,
            'id': addr_obj.id
        }
        return JsonResponse(addr_data)


@login_required()
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
            print('added')

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


def total_amount(request):
    if request.method == 'GET':

        cart = Cart.objects.filter(user=request.user)

        final_amount = 0
        for obj in cart:
            qyt_ins = obj.quantity
            amount_ins = obj.item.discounted
            final_amount += amount_ins * qyt_ins

        plus_delivery = final_amount + 50

        data = {
            'final_amount': final_amount,
            'plus_delivery': plus_delivery,
        }
    return JsonResponse(data)


def favorite_temp(request):
    favorite_obj = AddToFevorate.objects.filter(user=request.user)

    template = 'favorite_template.html'
    context = {
        'favorite_obj': favorite_obj,
    }

    return render(request, template_name=template, context=context)
