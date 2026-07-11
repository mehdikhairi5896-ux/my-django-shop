from django.contrib import admin
from .models import Product

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'image')  # نمایش تصویر در لیست محصولات
    search_fields = ('name',)

admin.site.register(Product, ProductAdmin)
