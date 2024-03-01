from django.db import models
from django.conf import settings
from recipes.models import Recipe

# Create your models here.

class RecipeComment(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='comments')
    likes = models.PositiveIntegerField(default=0, null=True)
    comment = models.TextField()
    rating = models.PositiveSmallIntegerField(null=True, blank=True, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Comment by {self.user.username} on {self.recipe.title}"

