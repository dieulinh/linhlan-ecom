from django.shortcuts import render
from django.http import JsonResponse,HttpResponse
from django.views.generic import ListView
from .models import Product, CartItem, Cart,Order
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from .forms import ProductForm
from django.contrib.auth.models import User
import os
import boto3
import uuid
import json
# Create your views here.
def retrieve_sqs_messages(request):
  print('RETRIEVE_MESSAGE')
  aws_access_key = os.environ.get('DJANGO_AWS_ACCESS_KEY')
  aws_secret_key = os.environ.get('DJANGO_AWS_SECRET_KEY')
  aws_region = 'us-east-1'
  # sns_topic_arn = 'arn:aws:sns:us-east-1:869830672968:mytopic_god.fifo'
  sqs_queue_url = 'arn:aws:sqs:us-east-1:869830672968:testq'
  sqs_queue_url = 'https://sqs.us-east-1.amazonaws.com/869830672968/testq'
  # Create an SQS client
  sqs_client = boto3.client('sqs', region_name=aws_region, aws_access_key_id=aws_access_key, aws_secret_access_key=aws_secret_key)
  print(sqs_client)
  try:
      # Receive messages from the SQS queue
      response = sqs_client.receive_message(
          QueueUrl=sqs_queue_url,
          MaxNumberOfMessages=10,  # Adjust as needed
          MessageAttributeNames=['All'],
          VisibilityTimeout=0,
          WaitTimeSeconds=0
      )

      # Check if there are messages in the response
      print(response)
      if 'Messages' in response:
          # Process the received message(s)
          for message in response['Messages']:
              
              message_body = message['Body']
              receipt_handle = message['ReceiptHandle']

              # Add your custom logic to handle the message content

              # Delete the message from the queue once processed (optional)
              sqs_client.delete_message(
                  QueueUrl=sqs_queue_url,
                  ReceiptHandle=receipt_handle
              )

          return HttpResponse('Messages retrieved and processed successfully with content'+message_body, status=200)
      else:
          return HttpResponse('No messages in the queue')

  except Exception as e:
      return HttpResponse(f'Error: {str(e)}', status=500)

def publish_to_sns(request):
  aws_access_key = os.environ.get('DJANGO_AWS_ACCESS_KEY')
  aws_secret_key = os.environ.get('DJANGO_AWS_SECRET_KEY')
  aws_region = 'us-east-1'
  sns_topic_arn = 'arn:aws:sns:us-east-1:869830672968:mytopic_god.fifo'
  sqs_queue_url = 'https://sqs.us-east-1.amazonaws.com/869830672968/testq'

  # Message to publish
  message = 'Hello, this is a test message from Django! hahaa'

  # Create an SNS client
  sns_client = boto3.client('sns', region_name=aws_region, aws_access_key_id=aws_access_key, aws_secret_access_key=aws_secret_key)
   # Create an SQS client
  sqs_client = boto3.client('sqs', region_name=aws_region, aws_access_key_id=aws_access_key, aws_secret_access_key=aws_secret_key)
  # Publish the message to the specified SNS topic
  response = sns_client.publish(
      TopicArn=sns_topic_arn,
      Message=message, MessageGroupId="Consumables",
      MessageDeduplicationId=str(uuid.uuid4()),
  )

  # Check if the message was successfully published
  print(response)
   # Message to send to SQS (you can customize this message)
  sqs_message = {
      'sns_message_id': response.get('MessageId'),
      'content': message
  }

  if 'MessageId' in response:
      sqs_response = sqs_client.send_message(
          QueueUrl=sqs_queue_url,
          MessageBody=json.dumps(sqs_message)
      )
      return HttpResponse(f'Message published successfully with ID: {response["MessageId"]}')
  else:
      return HttpResponse('Failed to publish message to SNS')
def list_s3(request):
  aws_access_key = os.environ.get('DJANGO_AWS_ACCESS_KEY')
  aws_secret_key = os.environ.get('DJANGO_AWS_SECRET_KEY')
  client = boto3.client('s3', aws_access_key_id=aws_access_key, aws_secret_access_key=aws_secret_key)

  response = client.list_objects(Bucket='freeway-devland')

  for content in response['Contents']:
      obj_dict = client.get_object(Bucket='freeway-devland', Key=content['Key'])
      print(content['Key'], obj_dict['LastModified'])
  return HttpResponse(content)

def view_cart(request):
  cart = request.session.get('cart', {})
  
  count = 0
  for key, products in cart.items():    
    count = count + products['quantity']
  return render(request,'products/view_cart.html', {'cart': cart, 'count': count})

@require_POST
def checkout(request):
  request.session = {}
  if request.method == 'POST':
    new_order = {}
    cart = Cart(user=User.objects.first())
    cart.save()
    total = 0
    for key, value in request.POST.items():
      if key.startswith('cart_items'):
        index = key.split('-')[1]
        if not request.POST[f'cart_items-{index}-product_id'] in new_order:
          new_order[request.POST[f'cart_items-{index}-product_id']] = {
            'name': request.POST[f'cart_items-{index}-name'],
            'quantity': request.POST[f'cart_items-{index}-quantity'],
            'product_id': request.POST[f'cart_items-{index}-product_id'],
          }
          product = Product.objects.get(pk=request.POST[f'cart_items-{index}-product_id'])
          cart_item = CartItem(
            quantity= request.POST[f'cart_items-{index}-quantity'],
            product_id=product,
            cart_it=cart
          )
          quantity = int(request.POST[f'cart_items-{index}-quantity'])
          price = int(product.stripe_price)
          cart_item.save()
          total += quantity * price
    print('Order')
    order = Order(cart_id=cart, total=total)
    order.save()
    print(total)
    print(new_order)
  return JsonResponse({
    'message': 'success'
  })
def home(request):
  return render(request,'products/home.html')
def details(request,product_id):
  product = Product.objects.get(pk=product_id)

  return render(request, "products/product_details.html", {'product': product})
def add_to_cart(request, product_id):
  product = Product.objects.get(pk=product_id)
  # Assume the cart is stored in the session as a list of product IDs
  cart = request.session.get('cart', {})
  pr_id = str(product_id)
  if pr_id in cart:
    cart[pr_id]['quantity'] = cart[pr_id]['quantity']+1
    print(cart[pr_id])
    if cart[pr_id]['price'] != int(product.stripe_price):
      cart[pr_id]['price'] = int(product.stripe_price)
  else:
    cart[pr_id] = {'quantity': 1, 'name': product.name, 'price': int(product.stripe_price) }
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

@csrf_exempt
@require_POST
def instant_checkout(request):
  try:
    payload = json.loads(request.body or '{}') if request.body else {}
  except json.JSONDecodeError:
    payload = {}

  product_id = payload.get('product_id') or request.POST.get('product_id')
  quantity = int(payload.get('quantity') or request.POST.get('quantity') or 1)

  if not product_id:
    return JsonResponse({'detail': 'product_id is required'}, status=400)

  try:
    product = Product.objects.get(pk=product_id)
  except Product.DoesNotExist:
    return JsonResponse({'detail': 'Product not found'}, status=404)

  user = User.objects.first()
  cart = Cart.objects.create(user=user)
  cart_item = CartItem.objects.create(quantity=quantity, product_id=product, cart_it=cart)

  total = int(product.price * 100) * quantity
  
  order = Order.objects.create(cart_id=cart, total=total)

  return JsonResponse({
    'order_id': order.id,
    'cart_id': cart.id,
    'cart_item_id': cart_item.id,
    'total': total,
    'currency': 'usd',
    'quantity': quantity,
    'product': {
      'id': product.id,
      'name': product.name,
      'price': float(product.price),
      'stripe_price': float(product.price) * 100,
      'image_url': product.image_url,
    },
  }, status=201)

class ProductList(ListView):
  model = Product
  http_method_names = ['get']

  def render_to_response(self, context, **response_kwargs):
    accept_header = self.request.headers.get('Accept', '')
    wants_json = 'application/json' in accept_header or '*/*' in accept_header or not accept_header

    if not wants_json:
      return JsonResponse({'detail': 'Not Acceptable. Send Accept: application/json.'}, status=406)

    products = context['object_list']

    def serialize(product):
      return {
        'id': product.id,
        'name': product.name,
        'handle': product.handle,
        'price': float(product.price),
        'og_price': float(product.og_price),
        'stripe_price': product.stripe_price,
        'stock': product.stock,
        'image_url': product.image_url,
        'updated_at': product.updated.isoformat(),
        'created_at': product.timestamp.isoformat(),
      }

    payload = {
      'count': len(products),
      'results': [serialize(product) for product in products],
    }

    return JsonResponse(payload, json_dumps_params={'ensure_ascii': False})
