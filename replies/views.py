from django.shortcuts import get_object_or_404 

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from replies.serializers import RecipeCommentReplySerializer
from replies.models import RecipeCommentReply

from comments.models import RecipeComment
from users.models import User

# Create your views here.

class ReplyCreateView(APIView):
    """
    Create a new reply to a comment.
    """
    def post(self, request, *args, **kwargs):
        user_id = request.data.get('user_id')
        parent_comment = request.data.get('parent_comment')

        if not user_id or not parent_comment:
            return Response({"error": "user_id and comment_id must be provided"}, status=status.HTTP_400_BAD_REQUEST)

        try: 
            comment = RecipeComment.objects.get(id=parent_comment)
        except RecipeComment.DoesNotExist:
            return Response({"error": "Comment not found"}, status=status.HTTP_404_NOT_FOUND)
        
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = RecipeCommentReplySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(parent_comment=comment, user=user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ReplyDetailView(APIView):
    """
    Retrieve, update, or delete a comment reply instance.
    """

    def get_object(self, pk):
        return get_object_or_404(RecipeCommentReply, pk=pk)

    def get(self, request, pk, *args, **kwargs):
        reply = self.get_object(pk)
        serializer = RecipeCommentReplySerializer(reply)
        return Response(serializer.data)

    def put(self, request, pk, *args, **kwargs):
        reply = self.get_object(pk)
        serializer = RecipeCommentReplySerializer(reply, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk, *args, **kwargs):
        reply = self.get_object(pk)
        serializer = RecipeCommentReplySerializer(reply, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, *args, **kwargs):
        reply = self.get_object(pk)
        reply.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)