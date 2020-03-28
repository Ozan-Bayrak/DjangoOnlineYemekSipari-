
from django.contrib import admin

# Register your models here.
from restaurant.models import Category, Restaurant, Foods, Images

class RestaurantImageInLine(admin.TabularInline):
    model = Images
    extra = 3

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'status']
    list_filter = ['status']

class RestaurantAdmin(admin.ModelAdmin):
    list_display = ['title', 'status','category','image_tag']
    readonly_fields = ('image_tag',)
    list_filter = ['status']
    inlines = [RestaurantImageInLine]


class FoodsAdmin(admin.ModelAdmin):
    list_display = ['title', 'status','price','restaurant','image']
    list_filter = ['status','restaurant']

class ImagesAdmin(admin.ModelAdmin):
    list_display = ['title','restaurant','image_tag']
    list_filter = ['restaurant']
    readonly_fields = ('image_tag',)

admin.site.register(Category,CategoryAdmin)
admin.site.register(Restaurant,RestaurantAdmin)
admin.site.register(Foods,FoodsAdmin)
admin.site.register(Images,ImagesAdmin)
