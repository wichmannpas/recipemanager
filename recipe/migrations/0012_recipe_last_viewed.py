# Generated by Django 3.1.1 on 2020-12-12 07:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipe', '0011_auto_20201114_1025'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='last_viewed',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
