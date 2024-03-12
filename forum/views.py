from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import ForumQuestion, ForumAnswer, Like
from users.models import User

from .serializers import ForumQuestionSerializer, ForumAnswerSerializer

# ForumQuestion Views
class ForumQuestionList(APIView):
    def get(self, request):
        questions = ForumQuestion.objects.all()
        serializer = ForumQuestionSerializer(questions, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ForumQuestionSerializer(data=request.data)
        if serializer.is_valid():
            user_id = request.data.get('user_id')
            if not user_id:
                return Response({"error": "User ID must be provided."}, status=status.HTTP_400_BAD_REQUEST)
        
            try:
                user = User.objects.get(id=user_id)
            except User.DoesNotExist:
                return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)

            serializer.save(user=user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ForumQuestionDetail(APIView):
    def get(self, request, pk):
        question = get_object_or_404(ForumQuestion, pk=pk)
        serializer = ForumQuestionSerializer(question)
        return Response(serializer.data)

    def put(self, request, pk):
        question = get_object_or_404(ForumQuestion, pk=pk)
        serializer = ForumQuestionSerializer(question, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        question = get_object_or_404(ForumQuestion, pk=pk)
        question.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# ForumAnswer Views
class ForumAnswerList(APIView):
    def post(self, request):
        serializer = ForumAnswerSerializer(data=request.data)
        if serializer.is_valid():
            user_id = request.data.get('user_id')
            if not user_id:
                return Response({"error": "User ID must be provided."}, status=status.HTTP_400_BAD_REQUEST)
        
            try:
                user = User.objects.get(id=user_id)
            except User.DoesNotExist:
                return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)

            serializer.save(user=user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ForumAnswerDetail(APIView):
    def get(self, request, pk):
        answer = get_object_or_404(ForumAnswer, pk=pk)
        serializer = ForumAnswerSerializer(answer)
        return Response(serializer.data)

    def put(self, request, pk):
        answer = get_object_or_404(ForumAnswer, pk=pk)
        serializer = ForumAnswerSerializer(answer, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        answer = get_object_or_404(ForumAnswer, pk=pk)
        answer.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class ForumQuestionLike(APIView):
    def post(self, request, pk):
        user_id = request.data.get('user_id')
        if not user_id:
            return Response({"error": "User ID must be provided."}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)

        question = get_object_or_404(ForumQuestion, pk=pk)
        like, created = Like.objects.get_or_create(user=user, question=question)

        if not created:
            # The user already liked this question, so unlike it.
            like.delete()
            return Response(
                {
                    'status': 'unliked'
                }
            )
        else:
            return Response({'status': 'liked'})

class ForumAnswerLike(APIView):
    def post(self, request, pk):
        user_id = request.data.get('user_id')
        if not user_id:
            return Response({"error": "User ID must be provided."}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)

        answer = get_object_or_404(ForumAnswer, pk=pk)
        like, created = Like.objects.get_or_create(user=user, answer=answer)

        if not created:
            # User already liked this answer, so unlike it.
            like.delete()
            return Response({'status': 'unliked'})
        else:
            # User has liked the answer.
            return Response({'status': 'liked'})