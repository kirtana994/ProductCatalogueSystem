from django.shortcuts import render

# Create your views here.

from rest_framework import viewsets
from .models import Product
from .serializers import ProductSerializer

#Perhaps you want to create a viewset for the Product model. Here's an example of how you can do that:
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all().order_by('id')
    serializer_class = ProductSerializer