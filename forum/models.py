from django.db import models
from django.conf import settings
from users.serializers import UserSerializer

# Create your models here.

class ForumQuestion(models.Model):
    # user = UserSerializer(read_only=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_question')
    text = models.TextField()

    # likes = models.PositiveIntegerField(default=0, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Forum question by {self.user.username} on {self.text}"

class ForumAnswer(models.Model):
    parent = models.ForeignKey(ForumQuestion, on_delete=models.CASCADE, related_name='answer')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='answer')
    text = models.TextField()

    # likes = models.PositiveIntegerField(default=0, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Answer by {self.user.username} on ForumQuestion {self.parent.id}"


class Like(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    question = models.ForeignKey(ForumQuestion, on_delete=models.CASCADE, related_name='likes', null=True, blank=True)
    answer = models.ForeignKey(ForumAnswer, on_delete=models.CASCADE, related_name='likes', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'question'), ('user', 'answer')
        indexes = [
            models.Index(fields=['user', 'question']),
            models.Index(fields=['user', 'answer']),
        ]
