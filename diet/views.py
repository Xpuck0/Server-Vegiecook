from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Diet
from .serializers import DietSerializer
from django.http import Http404

class DietListCreate(APIView):
    """
    List all diets, or create a new diet.
    """
    def get(self, request, format=None):
        diets = Diet.objects.all()
        serializer = DietSerializer(diets, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = DietSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DietDetail(APIView):
    """
    Retrieve, update or delete a diet instance.
    """
    def get_object(self, pk):
        try:
            return Diet.objects.get(pk=pk)
        except Diet.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        diet = self.get_object(pk)
        serializer = DietSerializer(diet)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        diet = self.get_object(pk)
        serializer = DietSerializer(diet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk, format=None):
        diet = self.get_object(pk)
        serializer = DietSerializer(diet, data=request.data, partial=True) # `partial=True` allows for partial updates
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        diet = self.get_object(pk)
        diet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
