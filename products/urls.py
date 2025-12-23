from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
  path('', views.home, name='home'),
  path('new_product/', views.create_product, name='newproduct'),
  path('list/', views.ProductList.as_view(), name='productlist'),
  path('<int:product_id>/', views.details, name='detail'),
  path('<int:product_id>/json/', views.product_detail_json, name='product_detail_json'),
  path('view_cart/', views.view_cart, name='view_cart'),
  path('checkout/', views.checkout, name='checkout'),
  path('list_s3/', views.list_s3, name='list_s3'),
  path('publish_to_sns/', views.publish_to_sns, name='publish_to_sns'),
  path('retrieve_sqs_messages/', views.retrieve_sqs_messages, name='retrieve_sqs_messages'),
  path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
  path('instant_checkout/', views.instant_checkout, name='instant_checkout'),
  path('cart_checkout/', views.cart_checkout, name='cart_checkout'),
  path('orders/', views.order_list, name='order_list'),
  path('orders/<int:order_id>/address/', views.save_order_address, name='save_order_address'),
]