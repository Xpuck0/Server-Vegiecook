from rest_framework import serializers
from diet.models import Diet


class DietSerializer(serializers.ModelSerializer):
    class Meta:
        model = Diet
        fields = '__all__'