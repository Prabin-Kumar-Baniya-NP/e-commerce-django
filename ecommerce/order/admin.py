from django.contrib import admin
from order.models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    fk_name = "order"


class CustomOrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemInline]


admin.site.register(Order, CustomOrderAdmin)
