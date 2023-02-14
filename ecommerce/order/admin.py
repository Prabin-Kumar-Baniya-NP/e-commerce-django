from django.contrib import admin
from order.models import Order, OrderItem
from payment.admin import PaymentInline


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    fk_ = "order"
    extra = 0
    readonly_fields = [
        "id",
        "order",
        "variant",
        "campaign",
        "quantity",
        "final_price",
        "currency",
        "created_at",
        "modified_at",
    ]

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False


class OrderAdmin(admin.ModelAdmin):
    list_filter = ["status"]
    inlines = [OrderItemInline, PaymentInline]
    readonly_fields = [
        "id",
        "user",
        "status",
        "shipping_address",
        "total_price",
        "currency",
        "created_at",
        "modified_at",
    ]


admin.site.register(Order, OrderAdmin)
