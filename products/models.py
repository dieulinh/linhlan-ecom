from django.db import models
from django.utils import timezone
from django.conf import settings
# Create your models here.
class Product(models.Model):
  user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1,on_delete=models.CASCADE)
  name = models.CharField(max_length=255)
  handle = models.SlugField(unique=True)
  price = models.DecimalField(max_digits=10, decimal_places=2, default=9.99)
  stripe_price = models.IntegerField(default=999)
  og_price = models.DecimalField(max_digits=10, decimal_places=2, default=9.99)
  stock = models.IntegerField()
  image_url = models.CharField(max_length=2083)
  timestamp = models.DateTimeField(auto_now_add=True)
  updated = models.DateTimeField(auto_now=True)
  def save(self, *args,**kwargs):
    if self.price != self.og_price:
      self.og_price = self.price
      self.stripe_price = int(self.price*100)
    super().save(*args, **kwargs)  
class Cart(models.Model):
  user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  def save(self, *args,**kwargs):
    if not self.id:
      self.created_at = timezone.now()
    self.updated_at = timezone.now()
    super().save(*args, **kwargs)  

class Offer(models.Model):
  code = models.CharField(max_length=10)
  description = models.CharField(max_length=255)
  discount = models.FloatField()

class CartItem(models.Model):
  product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
  quantity = models.IntegerField(default=1)
  cart_it = models.ForeignKey(Cart, on_delete=models.CASCADE)
