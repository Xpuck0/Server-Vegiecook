from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Recipe, RecipeComment 
from replies.models import RecipeCommentReply
from .serializers import RecipeCommentSerializer, RecipeCommentReplySerializer
from rest_framework import status
from users.models import User






class CommentCreateView(APIView):

    def post(self, request, *args, **kwargs):
        # Extract 'recipe_id' and 'user_id' from the request body
        recipe_id = request.data.get('recipe_id')
        user_id = request.data.get('user_id')

        if not recipe_id or not user_id:
            return Response({"error": "recipe_id and user_id are required"}, status=status.HTTP_400_BAD_REQUEST)

        # Fetch the user instance based on 'user_id'
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        # Now, 'user' is a User instance that can be correctly associated with the comment
        request.data['recipe'] = recipe_id
        # Instead of directly modifying request.data, pass 'user' to the serializer's save method
        serializer = RecipeCommentSerializer(data=request.data)
        if serializer.is_valid():
            # Pass 'user' instance directly to 'save' method
            serializer.save(user=user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CommentListView(APIView):

    def get(self, request, *args, **kwargs):
        recipe_id = kwargs.get('recipe_id')
        comments = RecipeComment.objects.filter(recipe_id=recipe_id)
        serializer = RecipeCommentSerializer(comments, many=True)
        return Response(serializer.data)


class CommentDetailView(APIView):

    def get_object(self, pk, recipe_id=None):
        return get_object_or_404(RecipeComment, pk=pk)

    def get(self, request, pk, recipe_id=None):
        comment = self.get_object(pk)
        serializer = RecipeCommentSerializer(comment)
        return Response(serializer.data)

    def put(self, request, pk, recipe_id=None):
        comment = self.get_object(pk)
        serializer = RecipeCommentSerializer(comment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk, recipe_id=None):
        comment = self.get_object(pk)
        serializer = RecipeCommentSerializer(comment, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, recipe_id=None):
        comment = self.get_object(pk)
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
