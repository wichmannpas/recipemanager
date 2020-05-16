# Generated by Django 3.0.6 on 2020-05-16 07:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipe', '0003_auto_20200516_0738'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipeingredient',
            name='unit',
            field=models.CharField(choices=[('g', 'g'), ('ml', 'ml'), ('l', 'l'), ('tl', 'TL'), ('el', 'EL')], default='g', max_length=10),
        ),
    ]
