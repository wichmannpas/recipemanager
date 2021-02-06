from django import forms

from .models import Recipe, RecipeInstance, RecipeInstanceImage


class RecipeFactorForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = (
            'display_factor',
        )


class RecipePortionsForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = (
            'portions',
        )


class RecipeInstanceForm(forms.ModelForm):
    class Meta:
        model = RecipeInstance
        fields = (
            'day',
            'notes',
        )
