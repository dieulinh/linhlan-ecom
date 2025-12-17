# shop/services.py
from decimal import Decimal
from django.db import transaction
from .models import CartItem, Order

class OrderService:
    @classmethod
    def create_order(cls, user):
        # Get user's cart items
        cart_items = CartItem.objects.filter(user=user)

        if not cart_items.exists():
            raise ValueError("No items in the cart")

        # Calculate total amount
        total_amount = sum(item.product.price * item.quantity for item in cart_items)

        # Create order transactionally
        with transaction.atomic():
            # Create order
            order = Order.objects.create(user=user, total_amount=total_amount)

            # Move cart items to order
            for cart_item in cart_items:
                order.orderitem_set.create(
                    product=cart_item.product,
                    quantity=cart_item.quantity,
                    price=cart_item.product.price
                )

            # Clear user's cart
            cart_items.delete()

        return order
