from datetime import date
from decimal import Decimal
from typing import Iterable

from django.db import models


class Tag(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self) -> str:
        return self.name


UNITS = (
    ('g', 'g'),
    ('ml', 'ml'),
    ('l', 'l'),
    ('tl', 'TL'),
    ('el', 'EL'),
    ('pieces', 'Stück'),
)

NUTRITIONAL = (
    ('kcal', 'kcal'),
    ('fat', 'Fett'),
    ('fat_saturated', 'gesä. Fettsäuren'),
    ('fat_monounsaturated', 'einf. ungesä. Fettsäuren'),
    ('fat_polyunsaturated', 'mehrf. ungesä. Fettsäuren'),
    ('carbohydrates', 'Kohlenhydrate'),
    ('sugar', 'Zucker'),
    ('fibres', 'Ballaststoffe'),
    ('protein', 'Eiweiß'),
    ('salt', 'Salz'),
    ('price', 'Preis (€)'),
)


class Ingredient(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self) -> str:
        return self.name


for nutritional_name, verbose_nutritional_name in NUTRITIONAL:
    for unit, verbose_unit in UNITS:
        Ingredient.add_to_class(
            '_'.join((nutritional_name, unit)),
            models.DecimalField(max_digits=15, decimal_places=8, null=True, blank=True)
        )


class RecipeIngredient(models.Model):
    class Meta:
        ordering = (
            'order_no',
        )
    recipe = models.ForeignKey(
        'Recipe', on_delete=models.CASCADE, related_name='recipe_ingredients')
    ingredient = models.ForeignKey(
        Ingredient, on_delete=models.CASCADE, related_name='recipe_ingredients')

    order_no = models.FloatField(default=1)
    amount = models.DecimalField(max_digits=10, decimal_places=3)
    unit = models.CharField(max_length=10, default='g', choices=UNITS)
    note = models.TextField(null=True, blank=True)


class Recipe(models.Model):
    name = models.CharField(max_length=80)
    tags = models.ManyToManyField(Tag, related_name='recipes')
    ingredients = models.ManyToManyField(Ingredient, through=RecipeIngredient)

    display_factor = models.DecimalField(
        max_digits=10, decimal_places=3, default=Decimal(1))

    portions = models.DecimalField(
        max_digits=10, decimal_places=3, default=Decimal(1))

    notes = models.TextField(null=True, blank=True)

    def __str__(self) -> str:
        return self.name

    def tag_str(self) -> str:
        return ', '.join(tag.name for tag in self.tags.all())

    @property
    def show_display_factor(self) -> bool:
        return self.display_factor != 1

    @property
    def nutritional_values(self):
        if not hasattr(self, '_nutritional_values'):
            list(self.ingredient_nutritional_values())
        return self._nutritional_values

    @property
    def nutritional_values_portion(self):
        if not hasattr(self, '_nutritional_values'):
            list(self.ingredient_nutritional_values())
        return [
            [nut / self.portions, incomplete]
            for nut, incomplete in self._nutritional_values
        ]

    def ingredient_nutritional_values(self) -> Iterable[list]:
        self._nutritional_values = [[0, False] for i in range(len(NUTRITIONAL))]

        for recipe_ingredient in self.recipe_ingredients.all():
            row = [recipe_ingredient.ingredient.name]
            for i, nut in enumerate(NUTRITIONAL):
                value = getattr(
                    recipe_ingredient.ingredient,
                    '_'.join((nut[0], recipe_ingredient.unit)))
                if value is None:
                    self._nutritional_values[i][1] = True
                else:
                    value *= recipe_ingredient.amount
                    self._nutritional_values[i][0] += value
                row.append(value)

            yield row


class RecipeInstance(models.Model):
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name='instances')
    day = models.DateField(default=date.today)
    notes = models.TextField(null=True, blank=True)
