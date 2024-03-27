from django.db import models

# Create your models here.
from django.core.validators import MinValueValidator

class Catalog(models.Model):
  title = models.CharField(max_length=255, null=False)
  description = models.TextField(blank=True)

  def __str__(self):
    return self.title

class Product(models.Model):
  title = models.CharField(max_length=255, null=False)
  price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.01)])
  warranty = models.PositiveIntegerField(blank=True, null=True)
  catalog_id = models.ForeignKey(Catalog, on_delete=models.CASCADE)
  description = models.TextField(blank=True)
  image = models.CharField(max_length=255, blank=True)
  SKU = models.CharField(max_length=255, primary_key=True)
  stock = models.PositiveIntegerField(default=0)
#   weight = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
#   dimensions = models.CharField(max_length=255, blank=True)

  def __str__(self):
    return self.title

class UserType(models.Model):
  type = models.CharField(max_length=255, unique=True)

  def __str__(self):
    return self.type

class User(models.Model):
  username = models.CharField(max_length=255, unique=True)
  email = models.EmailField(unique=True)
  contact = models.CharField(max_length=20)
  address = models.TextField(blank=True)
  # Password field should be replaced with a hashed password implementation
  password = models.CharField(max_length=255)
  user_type_id = models.ForeignKey(UserType, on_delete=models.CASCADE,default=1)
  first_name = models.CharField(max_length=255, blank=True)
  last_name = models.CharField(max_length=255, blank=True)
  created_date = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return self.username

class Order(models.Model):
  user_id = models.ForeignKey(User, on_delete=models.CASCADE)
  total_price = models.DecimalField(max_digits=10, decimal_places=2)
  discount_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
  payment_mode = models.CharField(max_length=255)
  ordered_date = models.DateTimeField(auto_now_add=True)
  coupon_code = models.CharField(max_length=255, blank=True)
  shipping_address = models.TextField(blank=True)
  order_status = models.CharField(max_length=255, default='placed')

  def __str__(self):
    return f"Order #{self.id} - {self.user.username}"

class ProductsOrders(models.Model):
  order_id = models.ForeignKey(Order, on_delete=models.CASCADE)
  product_sku = models.ForeignKey(Product, on_delete=models.CASCADE)
  quantity = models.PositiveIntegerField()

  class Meta:
    unique_together = (('order_id', 'product_sku'),)

  def __str__(self):
    return f"{self.quantity}x {self.product.title} (Order #{self.order.id})"
