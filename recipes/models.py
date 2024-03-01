from django.db import models
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from diet.models import Diet
from courses.models import Course
from categories.models import Category

# Create your models here.

# class RecipeCategory(models.Model):
#     name = models.CharField(max_length=100)
#     description = models.TextField(blank=True)

#     def __str__(self):
#         return self.name



class Recipe(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    diet = models.ForeignKey(Diet, on_delete=models.SET_NULL, null=True, blank=True, related_name='recipes')
    categories = models.ManyToManyField(Category, related_name='recipes', blank=True)
    courses = models.ManyToManyField(Course, related_name='recipes', blank=True) 

    title = models.CharField(max_length=255)

    image = models.ImageField(upload_to='recipe_hero')

    ingredients = models.JSONField(default=dict)
    instructions = models.JSONField(default=list)

    rating = models.DecimalField(max_digits=2, decimal_places=1, blank=True, null=True, validators=[MinValueValidator(0, 'Rating must be at least 0'), MaxValueValidator(5, 'Rating must not exceed 5')])
    votes = models.PositiveIntegerField(blank=True, null=True, default=0)

    description = models.TextField()
    serving_size = models.CharField()

    prep_time = models.DurationField()
    cook_time = models.DurationField()
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def total_time(self):
        return self.prep_time + self.cook_time

    def __str__(self):
        return f"{self.title} {self.user.username}"

class Image(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='image_set')
    image = models.ImageField(upload_to='images')
