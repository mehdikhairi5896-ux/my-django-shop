from django.contrib import admin
from .models import CartItem, Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'status', 'total_price_display', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('user__username',)
    inlines = [OrderItemInline]

    def total_price_display(self, obj):
        return f"{obj.total_price():,} تومان"

    total_price_display.short_description = "مبلغ کل"

    inlines = [OrderItemInline]


admin.site.register(CartItem)
admin.site.register(OrderItem)
