from django.contrib import admin

from .models import Item, Order, PastOrder, CouponCode

# Register your models here.

admin.site.register(Item)
admin.site.register(Order)
admin.site.register(PastOrder)
admin.site.register(CouponCode)