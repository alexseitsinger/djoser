from rest_framework.serializers import ModelSerializer

from .models import User

from djoser.serializers import UserSerializer as DjoserUserSerializer


class UserSerializer(DjoserUserSerializer):
    class Meta:
        model = User
        fields = ("username", "uuid", "email")
