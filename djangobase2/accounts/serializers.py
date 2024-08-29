from dj_rest_auth.serializers import LoginSerializer
from rest_framework import serializers
from .models import User


class CSLoginSerializer(LoginSerializer):
    username = None
    email = serializers.CharField(required=True, allow_blank=False)
    password = serializers.CharField(style={"input_type": "password"})


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "pk",
            "username",
            "email",
        ]
