from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name='index'),
    path("categories/", views.categories, name='categories'),
    path("cart", views.cart, name='cart'),
    path("checkout/", views.checkout, name='checkout'),
    path("contact/", views.contact, name='contact'),
    path("product/", views.prodcut, name='product')
]