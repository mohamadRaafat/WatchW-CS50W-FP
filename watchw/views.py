from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

# Create your views here.
def index(request):
    return render(request, "watchw/index.html")

def categories(request):
    return render(request, "watchw/categories.html")

def cart(request):
    return render(request, "watchw/cart.html")

def checkout(request):
    return render(request, "watchw/checkout.html")

def contact(request):
    return render(request, "watchw/contact.html")

def prodcut(request):
    # 7ot henna fel url parameter hayesta8al bel item id
    return render(request, "watchw/product.html")

