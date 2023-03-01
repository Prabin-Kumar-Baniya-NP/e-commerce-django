from django.contrib import admin
from category.models import Category


class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "is_active"]
    search_fields = ["name"]
    list_filter = ["is_active"]


admin.site.register(Category, CategoryAdmin)
