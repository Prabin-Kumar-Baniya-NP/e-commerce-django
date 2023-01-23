from django.contrib import admin
from product.models import Product, Variation


class VariationInline(admin.TabularInline):
    model = Variation
    fk_name = "product"


class CustomProductAdmin(admin.ModelAdmin):
    list_display = ["name", "is_active"]
    search_fields = ["name"]
    list_filter = ["category"]
    inlines = [VariationInline]


admin.site.register(Product, CustomProductAdmin)
