# Generated by Django 5.0.2 on 2024-02-10 19:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0002_alter_image_recipe'),
    ]

    operations = [
        migrations.DeleteModel(
            name='RecipeComment',
        ),
    ]