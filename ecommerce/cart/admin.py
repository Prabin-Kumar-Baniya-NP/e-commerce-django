from django.contrib import admin
from cart.models import Cart, CartItem


class CartItemInline(admin.TabularInline):
    model = CartItem
    fk_name = "cart"
    fields = ["product", "campaign"]


class CustomCartAdmin(admin.ModelAdmin):
    list_display = ["user"]
    inlines = [CartItemInline]


admin.site.register(Cart, CustomCartAdmin)
