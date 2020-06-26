from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name='index'),
    path("categories/<str:type>/", views.categories, name='categories'),
    path("cart", views.cart, name='cart'),
    path("checkout/", views.checkout, name='checkout'),
    path("apply_coupon/", views.apply_coupon, name='apply_coupon'),
    path("contact/", views.contact, name='contact'),
    path("product/<int:id>", views.prodcut, name='product'),
    path("add_item_to_cart/", views.add_item_to_cart, name='add_item_to_cart'),
    path("clear_user_cart/", views.clear_user_cart, name='clear_user_cart'),
    path('stripe_config/', views.stripe_config, name="stripe_config"),  # new
    path('create-checkout-session/', views.create_checkout_session, name='create-checkout-session'),  # new
    path('create-checkout-session/success/', views.after_stripe_success, name='success'),  # new
    path('create-checkout-session/cancelled/', views.after_stripe_cancelled, name='cancelled'),  # new
    path('past_orders/', views.past_orders, name='past_orders'),
    path('superuser_pending_orders/', views.superuser_pending_orders, name='superuser_pending_orders'),
    path('confirm_pending_order/', views.confirm_pending_order, name='confirm_pending_order'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register')
]
