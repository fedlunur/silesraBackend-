from django.shortcuts import render
from rest_framework import serializers, viewsets
from .models import Product
from .serializers import *
# Create your views here.
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
