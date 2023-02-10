from django.contrib import admin
from order.models import Order


class CustomOrderAdmin(admin.ModelAdmin):
    list_filter = ["status"]


admin.site.register(Order, CustomOrderAdmin)
