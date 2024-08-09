from django.contrib import admin

from publication.models import Public

@admin.register(Public)
class PublicAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "author",
        "informations",
        "created",
    )
    list_display_links = (
        "id",
        "author",
        "informations",
    )