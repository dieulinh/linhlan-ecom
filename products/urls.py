from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
  path('', views.home, name='home'),
  path('new_product/', views.create_product, name='newproduct'),
  path('list/', views.ProductList.as_view(), name='productlist'),
  path('<int:product_id>/', views.details, name='detail'),
  path('view_cart/', views.view_cart, name='view_cart'),
  path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
]