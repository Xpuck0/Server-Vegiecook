from django.db import transaction
from django.core.exceptions import ValidationError
from datetime import timedelta
from rest_framework import serializers
from .models import Recipe, Image

from comments.serializers import RecipeCommentSerializer
from users.models import User  # Assuming you have a custom user model
from users.serializers import UserSerializer
from diet.serializers import DietSerializer
from courses.serializers import CourseSerializer
from diet.models import Diet
from courses.models import Course
from categories.models import Category
from categories.serializers import CategorySerializer

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['id', 'image']

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['id', 'image']


class RecipeListSerializer(serializers.ModelSerializer):
    diet = DietSerializer(read_only=True)
    categories = CategorySerializer(many=True, read_only=True)

    class Meta:
        model = Recipe
        fields = ['id', 'title', 'image', 'diet', 'categories', 'rating', 'votes']

class RecipeSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    images = ImageSerializer(many=True, read_only=True, source='image_set')
    image = serializers.ImageField(max_length=None, use_url=True)
    comments = RecipeCommentSerializer(many=True, read_only=True)
    total_time = serializers.ReadOnlyField()
    prep_time = serializers.DurationField()
    cook_time = serializers.DurationField()
    categories = CategorySerializer(many=True, read_only=True)
    diet = DietSerializer(read_only=True)
    courses = CourseSerializer(many=True, read_only=True)

    # Assuming 'Category', 'Diet', and 'Course' are the related models
    category_ids = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        many=True,
        write_only=True,
        source='categories'
    )
    diet_id = serializers.PrimaryKeyRelatedField(
        queryset=Diet.objects.all(),
        write_only=True,
        source='diet'
    )
    course_ids = serializers.PrimaryKeyRelatedField(
        queryset=Course.objects.all(),
        many=True,
        write_only=True,
        source='courses'
    )

    class Meta:
        model = Recipe
        fields = '__all__'  # Ensure you include the new *_ids fields if you're specifying fields explicitly

    @transaction.atomic
    def create(self, validated_data):
        categories_data = validated_data.pop('categories')
        diet_data = validated_data.pop('diet')
        courses_data = validated_data.pop('courses')

        recipe = Recipe.objects.create(**validated_data)

        recipe.categories.set(categories_data)
        recipe.diet = diet_data
        recipe.save()
        recipe.courses.set(courses_data)

        return recipe

    @transaction.atomic
    def update(self, instance, validated_data):
        if 'categories' in validated_data:
            categories_data = validated_data.pop('categories')
            instance.categories.set(categories_data)

        if 'diet' in validated_data:
            diet_data = validated_data.pop('diet')
            instance.diet = diet_data
            instance.save()

        if 'courses' in validated_data:
            courses_data = validated_data.pop('courses')
            instance.courses.set(courses_data)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        return instance
