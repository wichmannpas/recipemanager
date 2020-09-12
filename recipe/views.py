from django.db.models import Prefetch
from django.shortcuts import get_object_or_404, render

from .models import Recipe, RecipeIngredient, Tag


def list_recipes(request):
    return render(request, 'recipe/index.html', {
        'recipes': Recipe.objects.order_by('name').prefetch_related(
            Prefetch('tags', Tag.objects.order_by('name'))
        ),
    })


def view_recipe(request, pk: int):
    recipe = get_object_or_404(Recipe.objects.prefetch_related(
        Prefetch('tags', Tag.objects.order_by('name')),
        Prefetch('recipe_ingredients', RecipeIngredient.objects.select_related('ingredient')),
    ), pk=pk)
    return render(request, 'recipe/view.html', {
        'recipe': recipe,
    })
