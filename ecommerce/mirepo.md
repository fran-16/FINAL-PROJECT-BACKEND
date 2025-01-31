---
repository:
  name: ecommerce
  owner: unknown
  url: ""
generated:
  timestamp: 2025-01-31T05:10:32.599Z
  tool: FlatRepo
statistics:
  totalFiles: 80
  totalLines: 1394
  languages: {}
  fileTypes:
    .txt: 1
    .py: 29
    .pyc: 50
---
```
=== EOF: requirements.txt

===  manage.py
```
#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
```
=== EOF: manage.py

===  users\__init__.py
```

```
=== EOF: users\__init__.py

===  users\views.py
```
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

```
=== EOF: users\views.py

===  users\urls.py
```
from django.urls import path
from .views import CustomTokenObtainPairView, RegisterView, UserListView  
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', RegisterView.as_view(), name='register'),
    path('users/', UserListView.as_view(), name='user_list'),
]
```
=== EOF: users\urls.py

===  users\tests.py
```
from django.test import TestCase

# Create your tests here.
```
=== EOF: users\tests.py

===  users\serializers.py
```
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
    def update(self, instance, validated_data):
        # Actualiza los campos del usuario con los datos validados
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.phone_number = validated_data.get('phone_number', instance.phone_number)
        instance.address = validated_data.get('address', instance.address)
        instance.profile_picture = validated_data.get('profile_picture', instance.profile_picture)
        instance.role = validated_data.get('role', instance.role)

        # Si se proporciona una nueva contraseña, la actualizamos
        password = validated_data.get('password', None)
        if password:
            instance.set_password(password)

        # Guardamos los cambios en la base de datos
        instance.save()
        return instance
        
```
=== EOF: users\serializers.py

===  users\models.py
```
from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ("user", "User"),
        ("admin", "Admin"),
        ("moderator", "Moderator"),
    )

    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)  
    profile_picture = models.ImageField(upload_to="profiles/", blank=True, null=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="user")  # Nuevo campo

    def __str__(self):
        return f"{self.username} - {self.role}"
```
=== EOF: users\models.py

===  users\apps.py
```
from django.apps import AppConfig


class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'
```
=== EOF: users\apps.py

===  users\admin.py
```
from django.contrib import admin

# Register your models here.
```
=== EOF: users\admin.py

===  products\__init__.py
```

```
=== EOF: products\__init__.py

===  products\views.py
```
from rest_framework import generics
from .models import Product
from .serializers import ProductSerializer

class ProductListCreateView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

```
=== EOF: products\views.py

===  products\urls.py
```
from django.urls import path
from .views import ProductListCreateView, ProductDetailView

urlpatterns = [
    path('', ProductListCreateView.as_view(), name='product-list'),  # Endpoint para listar y crear productos
    path('<int:pk>/', ProductDetailView.as_view(), name='product-detail'),  # Endpoint para obtener, actualizar o eliminar un producto

 ]
```
=== EOF: products\urls.py

===  products\tests.py
```
from django.test import TestCase

# Create your tests here.
```
=== EOF: products\tests.py

===  products\serializers.py
```
from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
```
=== EOF: products\serializers.py

===  products\models.py
```
from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=100, default="General")
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    image = models.URLField(null=True, blank=True)  # Permitir nulo y vacío para imagen
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
```
=== EOF: products\models.py

===  products\apps.py
```
from django.apps import AppConfig


class ProductsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'products'
```
=== EOF: products\apps.py

===  products\admin.py
```
from django.contrib import admin

# Register your models here.
```
=== EOF: products\admin.py

===  ecommerce\__init__.py
```

```
=== EOF: ecommerce\__init__.py

===  ecommerce\wsgi.py
```
"""
WSGI config for ecommerce project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce.settings')

application = get_wsgi_application()
```
=== EOF: ecommerce\wsgi.py

===  ecommerce\urls.py
```
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.permissions import AllowAny

# Configuración de Swagger
schema_view = get_schema_view(
    openapi.Info(
        title="Ecommerce API",
        default_version='v1',
        description="API documentation for the Ecommerce project",
    ),
    public=True,
    permission_classes=(AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('users.urls')),  # Rutas de autenticación
    path('api/products/', include('products.urls')),   
    # Ruta para la documentación interactiva
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]
```
=== EOF: ecommerce\urls.py

===  ecommerce\settings.py
```
"""
Django settings for ecommerce project.

Generated by 'django-admin startproject' using Django 3.2.7.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

from pathlib import Path
from datetime import timedelta

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-+67_t3f%x62bg$s!(bmq@wiqq+xnpm$h8!1q2()gxl6&m(zxcs'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'users',
    'products',
    'drf_yasg',
    "corsheaders",
]


REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
}


SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=60),  # Token dura 60 minutos
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),  # Refresh Token dura 7 días
    "ROTATE_REFRESH_TOKENS": True,  # Genera un nuevo refresh token al usarlo
    "BLACKLIST_AFTER_ROTATION": True,  # Invalida el refresh token después de usarlo
    "AUTH_HEADER_TYPES": ("Bearer",),  # Tipo de autenticación con "Bearer"
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
]


CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173", # Ajusta esto si tu frontend está en otro puerto
]

CORS_ALLOW_CREDENTIALS = True


ROOT_URLCONF = 'ecommerce.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'ecommerce.wsgi.application'
AUTH_USER_MODEL = 'users.CustomUser'

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'ecommerce_db',
        'USER': 'postgres',  # Usuario configurado
        'PASSWORD': '447870',  # Contraseña configurada al instalar PostgreSQL
        'HOST': 'localhost',  # Servidor local
        'PORT': '5432',       # Puerto predeterminado
    }
}
# esperenxd

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]




# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
```
=== EOF: ecommerce\settings.py

===  ecommerce\asgi.py
```
"""
ASGI config for ecommerce project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce.settings')

application = get_asgi_application()
```