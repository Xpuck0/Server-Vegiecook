# Generated by Django 5.0.2 on 2024-02-27 13:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('categories', '0001_initial'),
        ('recipes', '0005_remove_recipe_course_recipe_courses'),
    ]

    operations = [
        migrations.DeleteModel(
            name='RecipeCategory',
        ),
        migrations.AlterField(
            model_name='recipe',
            name='categories',
            field=models.ManyToManyField(blank=True, related_name='recipes', to='categories.category'),
        ),
    ]