from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password']

        extra_kwargs = {
            'password': {'write_only': True}
        }
        
    def create(self, data):
        password = data.pop('password', None)
        instance = self.Meta.model(**data)

        if password is not None:
            instance.set_password(password)
            instance.save()
        return instance