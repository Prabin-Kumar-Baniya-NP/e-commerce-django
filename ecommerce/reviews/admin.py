from django.contrib import admin
from reviews.models import Review


class CustomReviewAdmin(admin.ModelAdmin):
    fields = ["user", "product", "rating", "comment", "image", "is_approved"]
    list_display = ["user", "product", "rating"]
    list_filter = ["rating"]
    search_fields = [
        "product__name",
        "user__first_name",
        "user__middle_name",
        "user__last_name",
    ]
    readonly_fields = [
        "user",
        "product",
        "rating",
        "comment",
    ]


admin.site.register(Review, CustomReviewAdmin)
