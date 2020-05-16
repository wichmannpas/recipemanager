from django.contrib import admin
from django.db.models import Prefetch

from recipe.models import Ingredient, Recipe, RecipeIngredient, RecipeInstance, Tag

admin.site.register(Tag)


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = (
        'name',
    )
    search_fields = (
        'name',
    )


class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredient


class RecipeInstanceInline(admin.TabularInline):
    model = RecipeInstance


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'tag_str',
    )
    list_filter = (
        'tags',
    )
    search_fields = (
        'name',
    )

    inlines = (
        RecipeIngredientInline,
        RecipeInstanceInline,
    )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.prefetch_related(Prefetch('tags', Tag.objects.order_by('name')))
