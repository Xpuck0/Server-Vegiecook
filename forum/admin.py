from django.contrib import admin
from .models import ForumAnswer, ForumQuestion

# Register your models here.

admin.site.register(ForumAnswer)
admin.site.register(ForumQuestion)