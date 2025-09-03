from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.ModelSerializer):
    categories = serializers.StringRelatedField(many=True)  # نمایش اسم دسته‌بندی
    avatar = serializers.ImageField(read_only=True)

    class Meta:
        model = Product
        fields = [
            'id', 'title', 'avatar', 'is_enable', 'created_at', 'updated_at',
            'description', 'stars', 'price', 'is_stock',
            'is_new', 'is_off', 'off_price', 'categories'
        ]
