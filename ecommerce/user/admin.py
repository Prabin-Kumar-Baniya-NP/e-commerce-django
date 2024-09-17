from django.contrib import admin
from user.models import User, Address, OTP


class AddressInline(admin.TabularInline):
    model = Address
    fk_name = "user"


class OTPInline(admin.TabularInline):
    model = OTP
    fk_name = "user"
    readonly_fields = ["datetime", "email", "phone_number", 'count']
    fields = ["id", "user", "email", "phone_number", "count", "datetime"]


class UserAdmin(admin.ModelAdmin):
    fields = (
        ("first_name", "middle_name", "last_name"),
        ("date_of_birth", "gender"),
        ("email", "is_email_verified"),
        ("phone_number", "is_phone_number_verified"),
        ("image"),
        ("is_active"),
        ("is_staff"),
        ("is_superuser"),
    )
    inlines = [AddressInline, OTPInline]
    list_display = ["first_name", "middle_name", "last_name"]
    list_filter = ["is_email_verified", "is_phone_number_verified"]
    search_fields = ["first_name", "middle_name", "last_name", "email", "phone_number"]


admin.site.register(User, UserAdmin)
admin.site.register(Address)
