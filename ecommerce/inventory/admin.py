from django.contrib import admin
from inventory.models import Inventory


class CustomInventoryAdmin(admin.ModelAdmin):
    list_display = ["variant", "available", "sold"]
    search_fields = ["variant__name"]
    list_filter = ["variant__product__category__name"]
    readonly_fields = ["sold"]


admin.site.register(Inventory, CustomInventoryAdmin)
