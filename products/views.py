from django.shortcuts import render
from django.http import JsonResponse
from django.views.generic import ListView
from .models import Product
from .forms import ProductForm
# Create your views here.
def view_cart(request):
  print(request.session)
  cart = request.session.get('cart', {})
  total = 0
  for prod, cart_item in cart:
    total = total + cart_item['quantity']
  return render(request,'products/view_cart.html', {'cart': cart, 'count': total})
def home(request):
  return render(request,'products/home.html')
def details(request,product_id):
  product = Product.objects.get(pk=product_id)

  return render(request, "products/product_details.html", {'product': product})
def add_to_cart(request, product_id):
  product = Product.objects.get(pk=product_id)
  print(product)

    # Assume the cart is stored in the session as a list of product IDs
  cart = request.session.get('cart', {})
  pr_id = str(product_id)
  if pr_id in cart:
    cart[pr_id]['quantity'] = cart[pr_id]['quantity']+1
  else:
    cart[pr_id] = {'quantity': 0, 'name': product.name, 'price': product.price }
  print(cart)
  request.session['cart'] = cart

  return JsonResponse({'message': 'Product added to cart successfully'})

def create_product(request):
  form = ProductForm()
  if request.method == 'POST':
    form = ProductForm(request.POST)
    if form.is_valid():
      cd = form.cleaned_data
      product = Product(
        name = cd['name'],
        price=cd['price'],
        handle=cd['handle'],
        stock=cd['stock'],
        image_url=cd['image_url']
      )
      product.save()
      return JsonResponse({
        'message': 'success'
      })
  return render(request,'products/product_form.html', {'form': form})

class ProductList(ListView):
  model = Product
  template_name = 'products/product_list.html'
