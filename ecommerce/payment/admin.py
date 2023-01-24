from django.contrib import admin
from payment.models import Payment


class CustomPaymentAdmin(admin.ModelAdmin):
    list_display = ["order", "provider", "status"]
    search_fields = ["id"]
    list_filter = ["provider", "status"]


admin.site.register(Payment, CustomPaymentAdmin)
