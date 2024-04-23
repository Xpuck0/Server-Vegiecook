from django.shortcuts import get_object_or_404
from django.http import Http404
from django.db import transaction
from rest_framework.permissions import IsAuthenticated
from .serializers import RecipeSerializer, RecipeListSerializer, RecipeCommentSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.exceptions import NotAuthenticated
from rest_framework.permissions import IsAuthenticated
from users.models import User
from .models import Recipe 
from courses.models import Course
from categories.models import Category
from rest_framework.parsers import MultiPartParser, JSONParser
import json
import jwt

def check_auth(request):
    token = request.COOKIES.get('jwt')

    if not token:
        raise NotAuthenticated('Unaunthenticated!')
    
    try:
        payload = jwt.decode(token, 'secret', algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        raise NotAuthenticated('Unaunthenticated!')

class RecipeCreateView(APIView):

    @transaction.atomic
    def post(self, request, format=None):
        print(request.data)

        user_id = request.data.get('user_id')

        if not user_id:
            return Response({"error": "user_id are required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)


        # Convert category IDs from request to integers
        categories = request.data.getlist('category_ids')
        try:
            categories_ids = [int(id) for id in categories]
        except ValueError:
            return Response({"error": "Invalid category IDs"}, status=status.HTTP_400_BAD_REQUEST)

        courses = request.data.getlist('course_ids')
        try:
            courses_ids = [int(id) for id in courses]
        except ValueError:
            return Response({"error": "Invalid course IDs"}, status=status.HTTP_400_BAD_REQUEST)

        #get string data
        title = request.data.get('title')  # This should be a string
        description = request.data.get('description')  # This should be a string
        serving_size = request.data.get('serving_size')  # This should be a string

        # Get image file
        image = request.data.get('image')
        diet_id = request.data.get('diet_id')

        try:
            diet_id = int(diet_id)
        except ValueError:
            return Response({"error": "Invalid diet ID"}, status=status.HTTP_400_BAD_REQUEST)

        prep_time = request.data.get('prep_time')
        cook_time = request.data.get('cook_time')

        #Convert request time to duration field
        def convert_minutes_to_duration(minutes):
            hours, minutes = divmod(int(minutes), 60)
            return f"{hours:02d}:{minutes:02d}:00"

        # Example conversion
        prep_time_formatted = convert_minutes_to_duration(prep_time)
        cook_time_formatted = convert_minutes_to_duration(cook_time)

        # Parse ingredients and instructions from JSON-encoded strings
        ingredients = json.loads(request.data.get('ingredients'))  # Assuming ingredients is a JSON-encoded string representing an object
        instructions = json.loads(request.data.get('instructions'))  # Assuming instructions is a JSON-encoded string representing a list


        # Prepare data for serialization, including proper handling of many-to-many fields
        data = {
            **request.data,
            'title': title,
            'description': description,
            'serving_size': serving_size,
            'image': image,
            'prep_time': prep_time_formatted,
            'cook_time': cook_time_formatted,
            'user_id': user.id,
            'diet_id': diet_id,
            'category_ids': categories_ids,  # Ensure this is a list of integers
            'course_ids': courses_ids,
            'ingredients': ingredients,
            'instructions': instructions,
        }

        print(data)

        serializer = RecipeSerializer(data=data)
        if serializer.is_valid():
            serializer.save(user=user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Recipe
from .serializers import RecipeListSerializer

class UserRecipesView(APIView):

    def get(self, request, user_id):
        recipes = Recipe.objects.filter(user_id=user_id).prefetch_related('image_set', 'categories')
        serializer = RecipeListSerializer(recipes, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class RecipeListView(APIView):
    def get(self, request):
        # Existing diet filtering
        diet_id = request.query_params.get('diet')
        recipes = Recipe.objects.all()
        if diet_id is not None:
            recipes = recipes.filter(diet_id=diet_id)
        
        # Category filtering
        category_ids = request.query_params.get('categories')
        if category_ids:
            category_ids = category_ids.split(',')
            recipes = recipes.filter(categories__id__in=category_ids).distinct()
        
        # Order by created_at in descending order (latest first)
        recipes = recipes.order_by('-created_at')
        
        # Prefetch related fields
        recipes = recipes.prefetch_related('image_set', 'categories')
        
        # Serialize and return the response
        serializer = RecipeListSerializer(recipes, many=True)
        return Response(serializer.data)

class SortedRecipesView(APIView):
    """
    A view that returns recipes sorted by their rating.
    """

    def get(self, request):
        # Fetch recipes and order them by the 'rating' field in descending order.
        # Adjust '-rating' if your model uses a different field or mechanism for ratings.
        recipes = Recipe.objects.all().order_by('-rating').prefetch_related('image_set', 'categories')

        # Serialize the query set.
        serializer = RecipeListSerializer(recipes, many=True)

        # Return the serialized data.
        return Response(serializer.data, status=status.HTTP_200_OK)

class RecipeDetailView(APIView):
    def get_object(self, pk):
        return get_object_or_404(Recipe.objects.prefetch_related('image_set', 'categories'), pk=pk)

    def get(self, request, pk):
        recipe = self.get_object(pk)
        serializer = RecipeSerializer(recipe)
        return Response(serializer.data)

    def put(self, request, pk):
        recipe = self.get_object(pk)
        serializer = RecipeSerializer(recipe, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request, pk):
        recipe = self.get_object(pk)
        serializer = RecipeSerializer(recipe, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        recipe = self.get_object(pk)
        recipe.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
