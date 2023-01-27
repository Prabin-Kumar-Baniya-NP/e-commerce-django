from django.contrib import admin
from product.models import Product, ProductAttribute, ProductVariant


class ProductVariantInline(admin.TabularInline):
    model = ProductVariant
    fk_name = "product"


class CustomProductAdmin(admin.ModelAdmin):
    list_display = ["name", "is_active"]
    search_fields = ["name"]
    list_filter = ["category"]
    inlines = [ProductVariantInline]


admin.site.register(ProductAttribute)
admin.site.register(Product, CustomProductAdmin)
