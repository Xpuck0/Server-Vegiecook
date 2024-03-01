from django.conf import settings
from django.db import models
from comments.models import RecipeComment

# Create your models here.

class RecipeCommentReply(models.Model):
    parent_comment = models.ForeignKey(RecipeComment, on_delete=models.CASCADE, related_name='replies')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='replies')
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Reply by {self.user.username} on Comment {self.parent_comment.id}"
