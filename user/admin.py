from django.contrib import admin

from user.models import Profile, User

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "username",
        "email",
        "first_name",
        "last_name",
    )
    list_display_links = (
        "id",
        "username",
    )
    list_editable = (
        "email",
    )
    list_filter = (
        "is_superuser",
    )
    search_fields = (
        "username",
        "email",
        "last_name",
        "first_name",
    )
    empty_value_display = "..."

    fields = (
        "username",
        "email",
        ("first_name", "last_name")
    )

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "status_profile",
    )
    list_display_links = (
        "id",
        "user",
        "status_profile",
    )