from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.forms import ModelForm

from restaurant.models import Restaurant, Foods


class ShopCart(models.Model):
    user = models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    restaurant = models.ForeignKey(Restaurant,on_delete=models.SET_NULL,null=True)
    food = models.ForeignKey(Foods,on_delete=models.SET_NULL,null=True)
    quantity = models.IntegerField()

    def __str__(self):
        return self.food
    @property
    def amount(self):
        return (self.quantity * self.food.price)
    @property
    def price(self):
        return (self.food.price)

class ShopCartForm(ModelForm):
    class Meta:
        model = ShopCart
        fields = ['quantity']