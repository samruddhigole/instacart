from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Product, Order,User
from .serializers import ProductSerializer, OrderSerializer, UserSerializer,ProductsOrdersSerializer

class ProductList(APIView):
  def get(self, request, format=None):
    """
    Get all products.
    """
    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)

class ProductDetail(APIView):
  def post(self, request, format=None):
    """
    Create an Product.
    """
    data = request.data
    # data["catalog_id"] = data["catalog"]
    serializer = ProductSerializer(data=data)
    print(request.data)
    if serializer.is_valid():
      print("data is valid")
      serializer.save()
      return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
  
  def get(self, request, sku, format=None):
    """
    Get a product by SKU.
    """
    try:
      product = Product.objects.get(SKU=sku)
    except Product.DoesNotExist:
      return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = ProductSerializer(product)
    return Response(serializer.data)

class OrderList(APIView):
  def get(self, request, format=None):
    """
    Get all orders.
    """
    orders = Order.objects.all()
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data)

  

class OrderDetail(APIView):
  def get(self, request, pk, format=None):
    """
    Get an order by ID.
    """
    try:
      order = Order.objects.get(pk=pk)
    except Order.DoesNotExist:
      return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = OrderSerializer(order)
    return Response(serializer.data)
  
  def post(self, request, format=None):
    """
    Create an order.
    """

    # check product quantity 
    # verify with available quantity
    # if not fulfilling then return Products not available


    serializer = OrderSerializer(data=request.data)
    # print(request.data)
    if serializer.is_valid() :
        serializer.save()
    else:
        err = serializer.errors


        # if after save of s, something failed at s1
        # revert back s
        
        res = Response(serializer.data, status=status.HTTP_201_CREATED)
        print(serializer.data,"sdsdsdassdsd")
        tmp_data = request.data.copy()
        tmp_data["order_id"] = serializer.data["id"]
        serializer1 = ProductsOrdersSerializer(data=tmp_data)
        if serializer1.is_valid():
            serializer1.save()
            return res
    return Response(err, status=status.HTTP_400_BAD_REQUEST)
  

class UserList(APIView):
  def get(self, request, format=None):
    """
    Get all Users.
    """
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)

  def post(self, request, format=None):
    """
    Create an user.
    """
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserDetails(APIView):
  def get(self, request, pk, format=None):
    """
    Get an order by ID.
    """
    try:
      user = User.objects.get(pk=pk)
    except User.DoesNotExist:
      return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = UserSerializer(user)
    return Response(serializer.data)

def user_profile(request):
  user = User.objects.get(pk=request.user.id)  # Assuming user is authenticated
  # Retrieve user's orders or other relevant information
  context = {'user': user}
  return render(request, 'ecommerce/user_profile.html', context)
