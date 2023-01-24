from django.contrib import admin
from inventory.models import Inventory


class CustomInventoryAdmin(admin.ModelAdmin):
    list_display = ["product_varient", "available", "sold"]
    search_fields = ["product_varient__name"]
    list_filter = ["product_varient__product__category__name"]
    readonly_fields = ["sold"]


admin.site.register(Inventory, CustomInventoryAdmin)
