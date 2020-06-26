import stripe

from django.contrib import messages
from django.shortcuts import render, reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

# stripe
#=========================================================
from django.views.decorators.csrf import csrf_exempt  # new
from django.conf import settings  # new
from django.http.response import JsonResponse  # new
#========================================================

from .models import Item, Order, PastOrder, CouponCode
from decimal import Decimal
from datetime import datetime


def get_cart_items_count(request):
    try:
        order = Order.objects.get(user_id=request.user.id)
        count = order.items.count()
        return count
    except:
        return 0

# Create your views here.
def index(request):
    context = {
        "count": get_cart_items_count(request)
    }
    return render(request, "watchw/index.html", context)

def categories(request, type):
    context = {
        "watches": Item.objects.filter(type=type),
        "count": get_cart_items_count(request)
    }
    print(type)
    print(Item.objects.filter(type=type))
    return render(request, "watchw/categories.html", context)

def cart(request):
    context = {
        "count": get_cart_items_count(request),
    }
    try:
        order = Order.objects.get(user_id=request.user.id)
        context['items'] = order.items.all
        context['total_price'] = order.total_price
    except:
        pass
    
    return render(request, "watchw/cart.html", context)

def checkout(request):
    egypt_govs = ["Kalyobiya Governorate ", "Suez Governorate ", "Cairo Governorate ", "Alexandria Governorate ", "Sharqeia Governorate ", "Damietta Governorate ", "Kafr El Shiekh Governorate", "The Red Sea Governorate ", "El-Beheira Governorate ", "Assiut Governorate ", "Ismailia Governorate ", "New Valley Governorate ", "Qena Governorate ",
                  "South Sinai Governorate ", "Sohag Governorate ", "Fayoum Governorate ", "Bani Souwaif Governorate ", "Port-Said Governorate ", "Matrouh Governorate ", "Menia Governorate ", "Dakahliya Governorate ", "Aswan Governorate ", "North Sinai Governorate ", "Monofiya Governorate ", "Giza Governorate ", "Luxor Governorate ", "Al Gharbya Governorate"]
    context = {
        "count": get_cart_items_count(request),
        'total_price': Order.objects.get(user_id=request.user.id).total_price,
        'egypt_govs': egypt_govs
    }
    return render(request, "watchw/checkout.html", context)

def contact(request):
    context = {
        "count": get_cart_items_count(request)
    }
    return render(request, "watchw/contact.html", context)

def prodcut(request, id):
    context = {
        "count": get_cart_items_count(request),
        "product": Item.objects.get(pk=id)
    }
    # 7ot henna fel url parameter hayesta8al bel item id
    return render(request, "watchw/product.html", context)

def apply_coupon(request):
    if request.method == 'POST':
        code = request.POST.get('coupon_code')

        # check if this coupon is valid
        try:
            coupon_db = CouponCode.objects.get(coupon=code)
            # get the order then discount it by the coupon percentage
            order = Order.objects.get(user_id=request.user.id)
            order.total_price -= order.total_price*coupon_db.discount_percentage
            order.save()
            messages.success(request, f'{coupon_db.discount_percentage*100}% Coupon applied successfully.')
            return HttpResponseRedirect(reverse('cart'))
        except CouponCode.DoesNotExist:
            messages.success(request, 'Coupon not valid/Expired.')
            return HttpResponseRedirect(reverse('cart'))



#================================================
#################POST REQUESTS###################
#================================================
def add_item_to_cart(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            # get the id of the product to be added to the user's cart
            product_id = request.POST.get('product_id')
            item = Item.objects.get(pk=product_id)

            # if there's an existing order, add to it, else make a new order
            try:
                order = Order.objects.get(user_id=request.user.id)
                
                order.total_price += Decimal(item.price.replace(',', ''))
            except Order.DoesNotExist:
                order = Order(user_id=request.user.id, total_price=Decimal(item.price.replace(',', '')))
                order.save()

            order.items.add(item)
            order.save()
            return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "watchw/login.html", {"message": "You need to be logged in first!"})

def clear_user_cart(request):
    try:
        # clear the cart for that specific user
        order = Order.objects.get(user_id=request.user.id)
        order.delete()
    except:
        pass
    
    return HttpResponseRedirect(reverse('cart'))


# Stripe
@csrf_exempt
def stripe_config(request):
    if request.method == 'GET':
        stripe_config = {'publicKey': settings.STRIPE_PUBLISHABLE_KEY}
        return JsonResponse(stripe_config, safe=False)


@csrf_exempt
def create_checkout_session(request):
    if request.method == 'GET':
        # domain_url = 'http://127.0.0.1:8000/watchw/checkout/'
        # el satr dah hayedeni el full url el ana 3ndha
        domain_url = f"http://{request.META['HTTP_HOST']}{request.get_full_path()}"
        print(domain_url)

        stripe.api_key = settings.STRIPE_SECRET_KEY
        try:
            # getting the order item to be paid
            order = Order.objects.get(user_id=request.user.id)
            order_items = order.items.all()
            # price = int(order.total_price*100)

            # ana kont 3amel el shwya el gayeen dol ashan a list item item wana badfa3 f stripe
            # however, ana sheltaha w ha5aleeha bel total order price 3alatool ashan a2dar a adfa3 b3d applying el discount coupon
            # line_items = []
            # for i in range(order.items.count()):
            #     # removing commas from the number to be able to change it to an integer
            #     price = order_items[i].price.replace(',', '')
            #     price = int(float(price))*100
            #     line_items.append({
                    # 'name': order_items[i].name,
                    # 'quantity': 1,
                    # 'currency': 'EGP',
                    # 'amount': price,
            #     })

            price = int(float(order.total_price))*100
            # ?session_id={CHECKOUT_SESSION_ID} means the redirect will have the session ID set as a query param
            checkout_session = stripe.checkout.Session.create(
                success_url=domain_url +
                'success?session_id={CHECKOUT_SESSION_ID}',
                cancel_url=domain_url + 'cancelled/',
                payment_method_types=['card'],
                mode='payment',
                line_items=[{
                    'name': "WatchW Order",
                    'quantity': 1,
                    'currency': 'EGP',
                    'amount': price,
                }]
            )
            return JsonResponse({'sessionId': checkout_session['id']})
        except Exception as e:
            return JsonResponse({'error': str(e)})


def after_stripe_success(request):
    # get the order that was just paid
    order_done = Order.objects.get(user_id=request.user.id)
    # make an instance of the PastOrder model so that order can be viewed
    past_order = PastOrder(user_id=request.user.id, date=datetime.utcnow(), total_price=order_done.total_price)
    # i must save this object first to be able to use the many to many relationship
    past_order.save()
    # now i need to add all the items that was purchased, to this object
    for i in range(order_done.items.count()):
        past_order.items.add(order_done.items.all()[i])

    # then clear the user cart
    order_done.delete()

    context = {
        "count": get_cart_items_count(request),
        "message": "Payment Succeeded"
    }

    return render(request, "watchw/index.html", context)

def after_stripe_cancelled(request):
    context = {
        "count": get_cart_items_count(request),
        "message": "Payment Failed"
    }
    return render(request, "watchw/index.html", context)

def past_orders(request):
    context = {
        "count": get_cart_items_count(request)
    }
    # get all the past orders of this specific user
    past_orders = PastOrder.objects.filter(user_id=request.user.id)
    context["past_orders"] = past_orders
    return render(request, "watchw/past_orders.html", context)

def superuser_pending_orders(request):
    pending_orders = PastOrder.objects.filter(order_confirmed=False)
    context = {
        "count": get_cart_items_count(request),     
        "pending_orders": pending_orders
    }
    return render(request, "watchw/pending_orders.html", context)

def confirm_pending_order(request):
    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        try:
            order = PastOrder.objects.get(pk=order_id)
            order.order_confirmed = True
            order.save()
        except Order.DoesNotExist:
            pass
        
        return HttpResponseRedirect(reverse('superuser_pending_orders'))





#=======================================================
#==================USER REGISTRATION====================
#=======================================================

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('index'))
        else:
            return render(request, "watchw/login.html", {"message": "Invalid Credentials."})
    return render(request, "watchw/login.html")



def logout_view(request):
    logout(request)
    return render(request, "watchw/login.html", {"message": "Logged out."})

def register_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        username = request.POST['username']
        password = request.POST['password']
        user = User.objects.create_user(username, email, password)
        user.save()
        return render(request, "watchw/login.html", {"message": "Registered Successfully"})

    return render(request, "watchw/register.html")
