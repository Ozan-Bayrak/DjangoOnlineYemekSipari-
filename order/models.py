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

class Order(models.Model):
    STATUS = (
        ('New','New'),
        ('Accepted','Accepted'),
        ('Preaparing','Preaparing'),
        ('OnRoad','OnRoad'),
        ('Completed','Completed'),
        ('Canceled', 'Canceled'),
    )

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    code = models.CharField(max_length=5,editable=False)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    phone = models.CharField(max_length=20,blank=True)
    address = models.CharField(max_length=20, blank=True)
    total = models.FloatField()
    status = models.CharField(max_length=10, choices=STATUS, default='New')
    ip = models.CharField(blank=True, max_length=20)
    adminnote = models.CharField(blank=True,max_length=100)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.first_name

class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields =['first_name','last_name','address','phone']

class OrderProduct(models.Model):
    STATUS = (
        ('New','New'),
        ('Accepted','Accepted'),
        ('Canceled','Canceled'),
    )
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    foods = models.ForeignKey(Foods, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.FloatField()
    amount = models.FloatField()
    status = models.CharField(max_length=10, choices=STATUS, default='New')
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.foods.title