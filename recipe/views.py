from datetime import timedelta

from django.db.models import Prefetch
from django.http import HttpResponseBadRequest
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .forms import RecipeFactorForm, RecipePortionsForm
from .models import NUTRITIONAL, Recipe, RecipeIngredient, Tag


def list_recipes(request):
    return render(request, 'recipe/index.html', {
        'recipes': Recipe.objects.order_by('-view_count', 'name').prefetch_related(
            Prefetch('tags', Tag.objects.order_by('name'))
        ),
    })


def view_recipe(request, pk: int):
    recipe: Recipe = get_object_or_404(Recipe.objects.prefetch_related(
        Prefetch('tags', Tag.objects.order_by('name')),
        Prefetch('recipe_ingredients',
                 RecipeIngredient.objects.select_related('ingredient')),
    ), pk=pk)

    factor_form = RecipeFactorForm(instance=recipe)
    portions_form = RecipePortionsForm(instance=recipe)
    if request.method == 'POST':
        if 'display-factor-form' in request.POST:
            factor_form = RecipeFactorForm(instance=recipe, data=request.POST)
            if factor_form.is_valid():
                recipe = factor_form.save()
                return redirect('recipe:view_recipe', recipe.pk)
        elif 'portions-form' in request.POST:
            portions_form = RecipePortionsForm(instance=recipe, data=request.POST)
            if portions_form.is_valid():
                recipe = portions_form.save()
                return redirect('recipe:view_recipe', recipe.pk)
        else:
            return HttpResponseBadRequest('invalid form')

    now = timezone.now()
    update_fields = ['last_viewed']
    if not recipe.last_viewed or now - recipe.last_viewed > timedelta(hours=8):
        recipe.view_count += 1
        update_fields.append('view_count')
    recipe.last_viewed = now
    recipe.save(update_fields=update_fields)

    return render(request, 'recipe/view.html', {
        'recipe': recipe,
        'factor_form': factor_form,
        'portions_form': portions_form,
        'nutritional': NUTRITIONAL,
    })
