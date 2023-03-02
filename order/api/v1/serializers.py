from rest_framework import serializers
from order.models import CartDetail, ShippingMethod, CartItem, UserCart
from product.models import Product


class CartDetailSerializer(serializers.ModelSerializer):
    cart_id = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = CartDetail
        fields = ['cart_id', 'order_date', 'shipping_id', 'promotion_id', 'total_amount']


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['name',]


class UserCartSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserCart
        fields = "__all__"


class CartItemSerializer(serializers.ModelSerializer):
    # product = serializers.PrimaryKeyRelatedField(read_only=True)
    # cart_id = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = CartItem
        fields = "__all__"


class CartItemFormSerializer(serializers.Serializer):
    product_name = serializers.CharField(max_length=100)
    qty = serializers.IntegerField()
    cart_id = serializers.UUIDField()