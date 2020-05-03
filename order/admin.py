from django.contrib import admin

# Register your models here.
from order.models import ShopCart, OrderProduct, Order


class ShopCartAdmin(admin.ModelAdmin):
    list_display = ['user','restaurant','food','price','quantity','amount']
    list_filter = ['user']

class OrderProductline(admin.TabularInline):
    model = OrderProduct
    readonly_fields = ('user','restaurant','foods','price','quantity','amount')
    can_delete = False
    extra = 0

class OrderAdmin(admin.ModelAdmin):
    list_display = ['first_name','last_name','phone','total','status']
    list_filter = ['status']
    readonly_fields = ('user','address','phone','first_name','ip','total')
    inlines = [OrderProductline]

class OrderProductAdmin(admin.ModelAdmin):
    list_display = ['user','foods','restaurant','price','quantity','amount']
    list_filter = ['user']

admin.site.register(ShopCart,ShopCartAdmin)
admin.site.register(Order,OrderAdmin)
admin.site.register(OrderProduct,OrderProductAdmin)