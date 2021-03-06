from datetime import timedelta

from django.db.models import Prefetch
from django.http import HttpResponseBadRequest
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .forms import RecipeFactorForm, RecipeInstanceForm, RecipePortionsForm
from .models import NUTRITIONAL, Recipe, RecipeIngredient, RecipeInstanceImage, Tag


def list_recipes(request):
    recipes = Recipe.objects.all()
    tag_filter = request.GET.getlist('tags')
    for tag in tag_filter:
        recipes = recipes.filter(tags__name__iexact=tag)

    recipes = recipes.order_by('-view_count', 'name').prefetch_related(
        Prefetch('tags', Tag.objects.order_by('name'))
    )
    return render(request, 'recipe/index.html', {
        'tag_filter': tag_filter,
        'recipes': recipes,
    })


def view_recipe(request, pk: int):
    recipe: Recipe = get_object_or_404(Recipe.objects.prefetch_related(
        Prefetch('tags', Tag.objects.order_by('name')),
        Prefetch('recipe_ingredients',
                 RecipeIngredient.objects.select_related('ingredient')),
    ), pk=pk)

    factor_form = RecipeFactorForm(instance=recipe)
    portions_form = RecipePortionsForm(instance=recipe)
    new_instance_form = RecipeInstanceForm()
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
        elif 'new-instance-form' in request.POST:
            new_instance_form = RecipeInstanceForm(data=request.POST)
            if new_instance_form.is_valid():
                new_instance_form.instance.recipe = recipe
                new_instance_form.save()
                return redirect('recipe:view_recipe', recipe.pk)
        elif 'image_file' in request.FILES:
            try:
                instance = get_object_or_404(recipe.instances,
                                             pk=int(request.POST.get('recipe_instance_id',
                                                                     -1)))
            except ValueError:
                return HttpResponseBadRequest('invalid argument')
            RecipeInstanceImage.objects.create(
                recipe_instance=instance,
                image=request.FILES.get('image_file')
            )
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
        'new_instance_form': new_instance_form,
        'nutritional': NUTRITIONAL,
        'recipe_instances': recipe.instances.order_by('-day').prefetch_related('images'),
    })
