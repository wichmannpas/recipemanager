from django.db.models import Prefetch
from django.shortcuts import get_object_or_404, redirect, render

from .forms import RecipeFactorForm
from .models import Recipe, RecipeIngredient, Tag


def list_recipes(request):
    return render(request, 'recipe/index.html', {
        'recipes': Recipe.objects.order_by('name').prefetch_related(
            Prefetch('tags', Tag.objects.order_by('name'))
        ),
    })


def view_recipe(request, pk: int):
    recipe: Recipe = get_object_or_404(Recipe.objects.prefetch_related(
        Prefetch('tags', Tag.objects.order_by('name')),
        Prefetch('recipe_ingredients', RecipeIngredient.objects.select_related('ingredient')),
    ), pk=pk)

    factor_form = RecipeFactorForm(instance=recipe)
    if request.method == 'POST':
        factor_form = RecipeFactorForm(instance=recipe, data=request.POST)
        if factor_form.is_valid():
            recipe = factor_form.save()
            return redirect('recipe:view_recipe', recipe.pk)

    return render(request, 'recipe/view.html', {
        'recipe': recipe,
        'factor_form': factor_form,
    })
