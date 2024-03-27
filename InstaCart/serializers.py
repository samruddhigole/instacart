from rest_framework import serializers
from .models import Product, Catalog, UserType, User, Order, ProductsOrders

class CatalogSerializer(serializers.ModelSerializer):
  class Meta:
    model = Catalog
    fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
  catalog = CatalogSerializer(read_only=True)  # Nested serializer for Catalog

  class Meta:
    model = Product
    fields = '__all__'

class UserTypeSerializer(serializers.ModelSerializer):
  class Meta:
    model = UserType
    fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    # fields = ('id', 'username', 'email', 'first_name', 'last_name', 'user_type')
    fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
  user = UserSerializer(read_only=True)  # Nested serializer for User

  class Meta:
    model = Order
    fields = '__all__'

class ProductsOrdersSerializer(serializers.ModelSerializer):
  product = ProductSerializer(read_only=True)  # Nested serializer for Product
  order = OrderSerializer(read_only=True)  # Nested serializer for Order

  class Meta:
    model = ProductsOrders
    fields = '__all__'
