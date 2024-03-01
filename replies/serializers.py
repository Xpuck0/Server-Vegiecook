from rest_framework import serializers
from users.serializers import UserSerializer
from replies.models import RecipeCommentReply

class RecipeCommentReplySerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = RecipeCommentReply
        fields = ['id', 'parent_comment', 'user', 'comment', 'created_at', 'updated_at']
