from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import get_user_model
from rest_framework.generics import ListAPIView
from .models import CustomUser
from .serializers import CustomUserSerializer, RegisterSerializer

User = get_user_model()

# Personalizar el Token para incluir datos adicionales
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Agregar información del usuario al token
        token["username"] = user.username
        token["email"] = user.email
        token["role"] = user.role  # Agregar el rol del usuario
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        serializer = CustomUserSerializer(self.user)
        data["user"] = serializer.data  # Incluir datos completos del usuario en la respuesta
        return data

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

# Vista para registro de usuarios
class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({"message": "Usuario creado exitosamente", "user": serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Vista para listar usuarios (Solo accesible con autenticación)
class UserListView(ListAPIView):
    permission_classes = [IsAuthenticated]  # 🔒 Protegemos con JWT
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

