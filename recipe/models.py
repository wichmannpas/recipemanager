from datetime import date
from decimal import Decimal

from django.db import models


class Tag(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self) -> str:
        return self.name


class Ingredient(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self) -> str:
        return self.name


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(
        'Recipe', on_delete=models.CASCADE, related_name='recipe_ingredients')
    ingredient = models.ForeignKey(
        Ingredient, on_delete=models.CASCADE, related_name='recipe_ingredients')

    amount = models.DecimalField(max_digits=10, decimal_places=3)
    unit = models.CharField(max_length=10, default='g', choices=(
        ('g', 'g'),
        ('ml', 'ml'),
        ('l', 'l'),
        ('tl', 'TL'),
        ('el', 'EL'),
        ('pieces', 'Stück'),
    ))
    note = models.TextField(null=True, blank=True)


class Recipe(models.Model):
    name = models.CharField(max_length=80)
    tags = models.ManyToManyField(Tag, related_name='recipes')
    ingredients = models.ManyToManyField(Ingredient, through=RecipeIngredient)

    display_factor = models.DecimalField(
        max_digits=10, decimal_places=3, default=Decimal(1))

    notes = models.TextField(null=True, blank=True)

    def __str__(self) -> str:
        return self.name

    def tag_str(self) -> str:
        return ', '.join(tag.name for tag in self.tags.all())

    @property
    def show_display_factor(self) -> bool:
        return self.display_factor != 1


class RecipeInstance(models.Model):
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name='instances')
    day = models.DateField(default=date.today)
    notes = models.TextField(null=True, blank=True)
