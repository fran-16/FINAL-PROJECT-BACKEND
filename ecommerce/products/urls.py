from django.urls import path
from .views import ProductListCreateView, ProductDetailView

urlpatterns = [
    path('', ProductListCreateView.as_view(), name='product-list'),  # Endpoint para listar y crear productos
    path('<int:pk>/', ProductDetailView.as_view(), name='product-detail'),  # Endpoint para obtener, actualizar o eliminar un producto

 ]
