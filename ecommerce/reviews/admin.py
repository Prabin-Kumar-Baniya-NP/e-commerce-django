from django.contrib import admin
from reviews.models import Reviews


class ReviewAdmin(admin.ModelAdmin):
    fields = ["user", "product", "rating", "comment", "image", "is_approved"]
    list_display = ["user", "product", "rating", "is_approved"]
    list_filter = ["rating", "is_approved"]
    search_fields = [
        "product__name",
        "user__first_name",
        "user__middle_name",
        "user__last_name",
    ]


admin.site.register(Reviews, ReviewAdmin)
