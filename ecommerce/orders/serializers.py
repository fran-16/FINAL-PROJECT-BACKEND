from rest_framework import serializers
from .models import Order
from products.models import Product
from users.models import CustomUser

class OrderSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all())
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())
    
    class Meta:
        model = Order
        fields = '__all__'