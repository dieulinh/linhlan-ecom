from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import ListView
from .models import Product
# Create your views here.
def home(request):
  return HttpResponse('Hello')
class ProductList(ListView):
  model = Product
  template_name = 'products/product_list.html'