from django.db import models
from django.conf import settings

# Create your models here.

class ForumQuestion(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()

    likes = models.PositiveIntegerField(default=0, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Forum question by {self.user.username} on {self.text}"

class ForumAnswer(models.Model):
    parent = models.ForeignKey(ForumQuestion, on_delete=models.CASCADE, related_name='answer')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='answer')
    text = models.TextField()

    likes = models.PositiveIntegerField(default=0, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Answer by {self.user.username} on ForumQuestion {self.parent.id}"
