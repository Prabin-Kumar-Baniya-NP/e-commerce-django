from django.contrib import admin
from cart.models import Cart, CartItem


class CartItemInline(admin.TabularInline):
    model = CartItem
    fk_name = "cart"
    fields = ["variant", "campaign", "quantity"]


class CartAdmin(admin.ModelAdmin):
    list_display = ["user"]
    inlines = [CartItemInline]
    search_fields = ["user__first_name", "user__middle_name", "user__last_name"]


admin.site.register(Cart, CartAdmin)
