from rest_framework.serializers import ModelSerializer
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
import logging

logger = logging.getLogger('inventory')


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password', 'email']

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        logger.info(f"New user registration : {validated_data['username']}")
        return super().create(validated_data)
