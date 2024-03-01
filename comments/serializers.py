from rest_framework import serializers
from comments.models import RecipeComment
from users.serializers import UserSerializer
from replies.serializers import RecipeCommentReplySerializer


class RecipeCommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    replies = RecipeCommentReplySerializer(many=True, read_only=True)

    class Meta:
        model = RecipeComment
        fields = ['id', 'user', 'likes', 'comment', 'replies', 'recipe', 'rating', 'created_at', 'updated_at']
        # fields = '__all__'