from rest_framework import serializers
from .models import CustomUser

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["id", "username", "email", "phone_number", "address", "profile_picture", "role"]  # Agregado role

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = CustomUser
        fields = ["id", "username", "email", "password", "phone_number", "address", "profile_picture", "role"]

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            username=validated_data["username"],
            email=validated_data.get("email", ""),
            password=validated_data["password"],
            phone_number=validated_data.get("phone_number", ""),
            address=validated_data.get("address", ""),
            profile_picture=validated_data.get("profile_picture", None),
            role=validated_data.get("role", "user")  # Se asigna el rol predeterminado si no se proporciona
        )
        return user
