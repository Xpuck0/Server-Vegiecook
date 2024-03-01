from django.contrib import admin
from comments.models import RecipeComment

# Register your models here.

@admin.register(RecipeComment)
class RecipeCommentAdmin(admin.ModelAdmin):
    pass