# Generated by Django 3.0.6 on 2020-05-30 16:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipe', '0005_auto_20200530_1801'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipeingredient',
            name='unit',
            field=models.CharField(choices=[('g', 'g'), ('ml', 'ml'), ('l', 'l'), ('tl', 'TL'), ('el', 'EL'), ('pieces', 'Stück')], default='g', max_length=10),
        ),
    ]
