from django import forms

from .models import Recipe


class RecipeFactorForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = (
            'display_factor',
        )
