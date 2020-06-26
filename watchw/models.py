import string
import random

from django.db import models

WATCH_TYPES = (
    ("Casual", "Casual"),
    ("Dress", "Dress"),
    ("Sports", "Sports"),
    ("Smart", "Smart"),
)

# Create your models here.
class Item(models.Model):
    type = models.CharField(max_length=25, choices=WATCH_TYPES)
    name = models.CharField(max_length=128)
    product_description = models.TextField()
    price = models.CharField(max_length=12)
    main_image_url = models.TextField()
    sub_image_url1 = models.TextField()
    sub_image_url2 = models.TextField()

    def __str__(self):
        return f"{self.type} - {self.name}"

class Order(models.Model):
    user_id = models.IntegerField()
    items = models.ManyToManyField(Item, blank=True, related_name='order')
    total_price = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return f"{self.items} - {self.user_id}"



class PastOrder(models.Model):
    user_id = models.IntegerField()
    items = models.ManyToManyField(Item, blank=True, related_name='past_orders')
    date = models.DateTimeField()
    order_confirmed = models.BooleanField(default=False)
    total_price = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return f"{self.user_id} - {self.order_confirmed} - {self.date}"

# function to generate a random string for a coupon code
def id_generator(size=8, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))
# e3ml coupons gdeeda mn el shell: : id_generator() :D



class CouponCode(models.Model):
    coupon = models.CharField(max_length=10)
    discount_percentage = models.DecimalField(max_digits=4, decimal_places=2)

    def __str__(self):
        return self.coupon
    

    
