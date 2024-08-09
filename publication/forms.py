from typing import Any
from django import forms

from publication.models import Public

class PublicUpdateCreateForm(forms.ModelForm):
    class Meta:
        model = Public
        fields = [
            "images_public",
            "informations",
        ]