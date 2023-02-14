from django.contrib import admin
from payment.models import Payment


class PaymentInline(admin.TabularInline):
    model = Payment
    fk_name = "order"
    readonly_fields = ["provider", "status", "created_at", "modified_at"]
    extra = 0

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False
