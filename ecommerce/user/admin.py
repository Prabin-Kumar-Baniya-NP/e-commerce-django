from django.contrib import admin
from user.models import User, Address


class AddressInline(admin.TabularInline):
    model = Address
    fk_name = "user"


class CustomUserAdmin(admin.ModelAdmin):
    fields = (
        ("first_name", "middle_name", "last_name"),
        ("date_of_birth", "gender"),
        ("email", "is_email_verified"),
        ("phone_number", "is_phone_number_verified"),
        ("photo"),
        ("is_active"),
        ("is_staff"),
        ("is_superuser"),
    )
    inlines = [AddressInline]


admin.site.register(User, CustomUserAdmin)
