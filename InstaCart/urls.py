from django.urls import path

from . import views

urlpatterns = [
    # path("", views.index, name="index"),
    path('products/', views.ProductList.as_view(), name='product_list'),
    path('product/create/', views.ProductDetail.as_view(), name='product_detail'),
    path('products/<str:sku>/', views.ProductDetail.as_view(), name='product_detail'),
    
    path('orders/', views.OrderList.as_view(), name='order_list'),
    path('orders/create/', views.OrderDetail.as_view(), name='order_detail'),
    path('orders/<int:pk>/', views.OrderDetail.as_view(), name='order_detail'),

    path('users/', views.UserDetails.as_view(), name='user_detail'),
    path('users/create/', views.UserList.as_view(), name='user_list'),
    path('users/<int:pk>/', views.UserList.as_view(), name='user_list'),

]
