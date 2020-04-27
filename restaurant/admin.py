
from django.contrib import admin

# Register your models here.
from django.utils.html import format_html
from mptt.admin import MPTTModelAdmin, DraggableMPTTAdmin

from restaurant.models import Category, Restaurant, Foods, Images, Comment


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
    list_display = ['title', 'status','price','restaurant','image_tag']
    list_filter = ['status','restaurant']
    readonly_fields = ('image_tag',)

class ImagesAdmin(admin.ModelAdmin):
    list_display = ['title','restaurant','image_tag']
    list_filter = ['restaurant']
    readonly_fields = ('image_tag',)

class CategoryAdmin2(DraggableMPTTAdmin):
    mptt_indent_field = "title"
    list_display = ('tree_actions', 'indented_title',
                    'related_products_count', 'related_products_cumulative_count')
    list_display_links = ('indented_title',)
    prepopulated_fields = {'slug': ('title',)}

    def get_queryset(self, request):
        qs = super().get_queryset(request)

        # Add cumulative product count
        qs = Category.objects.add_related_count(
                qs,
                Restaurant,
                'category',
                'products_cumulative_count',
                cumulative=True)

        # Add non cumulative product count
        qs = Category.objects.add_related_count(qs,
                 Restaurant,
                 'category',
                 'products_count',
                 cumulative=False)
        return qs

    def related_products_count(self, instance):
        return instance.products_count
    related_products_count.short_description = 'Related products (for this specific category)'

    def related_products_cumulative_count(self, instance):
        return instance.products_cumulative_count
    related_products_cumulative_count.short_description = 'Related products (in tree)'

class CommentAdmin(admin.ModelAdmin):
    list_display=['subject','comment','restaurant','user','status']
    list_filter = ['status']

admin.site.register(Category,CategoryAdmin2)
admin.site.register(Restaurant,RestaurantAdmin)
admin.site.register(Foods,FoodsAdmin)
admin.site.register(Images,ImagesAdmin)
admin.site.register(Comment,CommentAdmin)
