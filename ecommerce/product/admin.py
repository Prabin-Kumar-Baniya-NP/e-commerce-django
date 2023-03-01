from django.contrib import admin
from product.models import Product, ProductAttribute, ProductVariant


class ProductVariantInline(admin.TabularInline):
    model = ProductVariant
    fk_name = "product"


class ProductAttributeAdmin(admin.ModelAdmin):
    list_display = ["name", "value"]
    search_fields = ["name"]
    list_filter = ["name"]


class ProductAdmin(admin.ModelAdmin):
    list_display = ["name", "is_active"]
    search_fields = ["name"]
    list_filter = ["category"]
    inlines = [ProductVariantInline]


admin.site.register(ProductAttribute, ProductAttributeAdmin)
admin.site.register(Product, ProductAdmin)
