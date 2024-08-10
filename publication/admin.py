from django.contrib import admin

from publication.models import Comment, Public

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

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "publications",
        "author_comment",
        "create_date_comment",
        "text",
    )
    list_display_links = (
        "id",
        "publications",
        "author_comment",
        "create_date_comment",
        "text",
    )