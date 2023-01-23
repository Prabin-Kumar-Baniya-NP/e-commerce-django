from django.contrib import admin
from product.models import Product


class CustomProductAdmin(admin.ModelAdmin):
    list_display = ["name", "price", "is_active"]
    search_fields = ["name"]
    list_filter = ["category"]


admin.site.register(Product, CustomProductAdmin)
