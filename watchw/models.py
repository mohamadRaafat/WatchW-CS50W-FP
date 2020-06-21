from django.db import models

# Create your models here.
class Item(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name

class Order(models.Model):
    user_id = models.IntegerField()
    items = models.ManyToManyField(Item, blank=True, related_name='order')

    def __str__(self):
        return f"{self.items} - {self.user_id}"