from django.contrib import admin

from .models import ExtraDropRule


@admin.register(ExtraDropRule)
class ExtraDropRuleAdmin(admin.ModelAdmin):
    list_display = ("trigger_ball", "drop_ball", "chance", "enabled")
    list_editable = ("chance", "enabled")
    list_filter = ("enabled",)
    list_select_related = ("trigger_ball", "drop_ball")
    search_fields = ("trigger_ball__country", "drop_ball__country")
    autocomplete_fields = ("trigger_ball", "drop_ball")

    fieldsets = (
        (None, {"fields": ("trigger_ball", "drop_ball", "chance", "enabled")}),
        (
            "Announcement message",
            {
                "description": "Customize the embed sent when the extra drop happens. "
                "Placeholders: {ball} = the caught ball, {drop} = the dropped ball, {user} = the player's name.",
                "fields": ("message_title", "message_description"),
            },
        ),
    )