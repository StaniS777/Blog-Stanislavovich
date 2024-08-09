from typing import Any
from django import forms

from publication.models import Comment, Public

class PublicUpdateCreateForm(forms.ModelForm):
    class Meta:
        model = Public
        fields = [
            "images_public",
            "informations",
        ]


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = [
            "text",
        ]