from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import Product, Review, Cart, CartItem, Order, OrderItem


@admin.register(Product)
class ProductAdmin(SummernoteModelAdmin):

    list_display = ('title', 'slug')
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title',)}
    summernote_fields = ('features',)


# Register your models here.
admin.site.register(Review)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Order)
admin.site.register(OrderItem)
