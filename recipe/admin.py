from django.contrib import admin, messages
from django.db import transaction
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

    @transaction.atomic
    def merge_ingredients(self, request, queryset):
        if len(queryset) < 2:
            self.message_user(
                request, 'At least two ingredients need to be selected!', messages.WARNING)
            return
        main = queryset.first()
        others = queryset[1:]
        len_others = len(others)
        RecipeIngredient.objects.filter(ingredient__in=others).update(ingredient=main)
        Ingredient.objects.filter(pk__in=[i.pk for i in others]).delete()
        self.message_user(
            request, '{} ingredients were merged into {}'.format(len_others, main),
            messages.SUCCESS)

    merge_ingredients.short_description = 'Merge selected ingredients'
    actions = (
        merge_ingredients,
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
