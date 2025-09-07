from rest_framework import serializers
from .models import (
    Category,
    Product,
    File,
    Cart,
    CartItem,
    Comment,
    Contact,
    Customer,
    Order,
    OrderItem,
)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = Category


class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = "__all__"


class ProductSerializer(serializers.ModelSerializer):
    categories = serializers.StringRelatedField(many=True)
    avatar = serializers.ImageField(read_only=True)

    class Meta:
        model = Product
        fields = [
            "id",
            "title",
            "avatar",
            "is_enable",
            "created_at",
            "updated_at",
            "description",
            "stars",
            "price",
            "is_stock",
            "is_new",
            "is_off",
            "off_price",
            "categories",
        ]


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = "__all__"


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = "__all__"


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = "__all__"


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = "__all__"
