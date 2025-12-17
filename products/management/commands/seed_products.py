import random
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from products.models import Product


class Command(BaseCommand):
    help = "Seed the database with sample products for the frontend client."

    def handle(self, *args, **options):
        user_model = get_user_model()
        user, _ = user_model.objects.get_or_create(
            username="demo",
            defaults={"email": "demo@example.com"},
        )
        if not user.has_usable_password():
            user.set_password("demo1234")
            user.save()

        catalog = [
            {
                "name": "Minimal Desk Lamp",
                "handle": "minimal-desk-lamp",
                "price": 48.00,
                "stock": 42,
                "image_url": "https://images.unsplash.com/photo-1524758631624-e2822e304c36?auto=format&fit=crop&w=800&q=80",
            },
            {
                "name": "Cotton Crew Tee",
                "handle": "cotton-crew-tee",
                "price": 22.00,
                "stock": 120,
                "image_url": "https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?auto=format&fit=crop&w=800&q=80",
            },
            {
                "name": "Wireless Earbuds",
                "handle": "wireless-earbuds",
                "price": 129.00,
                "stock": 58,
                "image_url": "https://images.unsplash.com/photo-1585386959984-a4155224a1ad?auto=format&fit=crop&w=800&q=80",
            },
            {
                "name": "Stoneware Mug",
                "handle": "stoneware-mug",
                "price": 18.00,
                "stock": 200,
                "image_url": "https://images.unsplash.com/photo-1556910103-1c02745aae4d?auto=format&fit=crop&w=800&q=80",
            },
            {
                "name": "Canvas Backpack",
                "handle": "canvas-backpack",
                "price": 78.00,
                "stock": 67,
                "image_url": "https://images.unsplash.com/photo-1489515217757-5fd1be406fef?auto=format&fit=crop&w=800&q=80",
            },
        ]

        created = 0
        for item in catalog:
            product, made = Product.objects.get_or_create(
                handle=item["handle"],
                defaults={
                    "user": user,
                    "name": item["name"],
                    "price": item["price"],
                    "og_price": item["price"],
                    "stock": item["stock"],
                    "image_url": item["image_url"],
                },
            )
            if made:
                created += 1
            else:
                # update price/stock to keep the demo aligned
                product.price = item["price"]
                product.og_price = item["price"]
                product.stock = item["stock"]
                product.image_url = item["image_url"]
                product.save()

        self.stdout.write(self.style.SUCCESS(f"Seed complete: {created} created, {len(catalog) - created} refreshed."))
