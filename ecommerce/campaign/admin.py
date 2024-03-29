from django.contrib import admin
from campaign.models import Campaign


class CampaignAdmin(admin.ModelAdmin):
    fields = (
        ("name"),
        ("description"),
        ("product"),
        ("discount"),
        ("start_datetime", "end_datetime"),
        ("promocode"),
        ("auto_apply"),
        ("is_active"),
    )
    list_display = ["name", "is_active", "start_datetime", "end_datetime"]
    search_fields = ["name", "promocode"]
    list_filter = ["is_active", "auto_apply"]



admin.site.register(Campaign, CampaignAdmin)
