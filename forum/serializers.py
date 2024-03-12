from rest_framework import serializers
from .models import ForumQuestion, ForumAnswer
from users.serializers import UserSerializer
from django.conf import settings
from django.db import models


class ForumAnswerSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    likes_count = serializers.SerializerMethodField()

    class Meta:
        model = ForumAnswer
        fields = '__all__'

    def get_likes_count(self, obj):
        return obj.likes.count()


class ForumQuestionSerializer(serializers.ModelSerializer):
    # user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='forum_questions')
    user = UserSerializer(read_only=True)
    answers = ForumAnswerSerializer(many=True, read_only=True, source='answer')

    likes_count = serializers.SerializerMethodField()

    class Meta:
        model = ForumQuestion
        fields = '__all__'

    def get_likes_count(self, obj):
        return obj.likes.count()