from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .serializers import CustomUserSerializer

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Puedes agregar campos personalizados al token si deseas
        token['username'] = user.username
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        serializer = CustomUserSerializer(self.user)
        data['user'] = serializer.data  # Agrega información del usuario al response
        return data

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
