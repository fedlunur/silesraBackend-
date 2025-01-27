from rest_framework import serializers, viewsets
from .models import Product, SubcategoryProperty

class ProductSerializer(serializers.ModelSerializer):
    properties = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'name', 'category', 'subcategory', 'price', 'image_url', 'sell_or_rent', 'description', 'contact', 'payment_status', 'properties']

    def get_properties(self, obj):
        properties = SubcategoryProperty.objects.filter(subcategory=obj.subcategory)
        return {prop.property_name: prop.value for prop in properties}
