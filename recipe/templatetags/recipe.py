from typing import Union

from django import template

from recipe.models import Recipe

register = template.Library()


@register.filter
def apply_display_factor(value: Union[float, int], recipe: Recipe) -> Union[float, int]:
    return value * recipe.display_factor
