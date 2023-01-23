from django.contrib import admin
from category.models import Category


class CustomCategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "is_active"]
    search_fields = ["name", "description"]
    list_filter = ["is_active"]


admin.site.register(Category, CustomCategoryAdmin)
