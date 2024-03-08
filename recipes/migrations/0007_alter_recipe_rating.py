# Generated by Django 5.0.2 on 2024-03-08 14:36

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0006_delete_recipecategory_alter_recipe_categories'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='rating',
            field=models.DecimalField(blank=True, decimal_places=1, default=0, max_digits=2, validators=[django.core.validators.MinValueValidator(0, 'Rating must be at least 0'), django.core.validators.MaxValueValidator(5, 'Rating must not exceed 5')]),
        ),
    ]
