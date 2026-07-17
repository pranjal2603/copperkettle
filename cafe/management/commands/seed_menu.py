from pathlib import Path

from django.conf import settings
from django.core.files import File
from django.core.management.base import BaseCommand

from cafe.models import MenuCategory, MenuItem


def attach_image(item, filename):
    image_path = Path(settings.MEDIA_ROOT) / "menu" / filename

    if not image_path.exists():
        print(f"❌ Image not found: {image_path}")
        return

    with image_path.open("rb") as f:
        item.image.save(
            image_path.name,
            File(f),
            save=False,
        )

    item.save(update_fields=["image"])
    print(f"🖼 Uploaded {filename}")


class Command(BaseCommand):
    help = "Seed Copper Kettle menu."

    def handle(self, *args, **kwargs):

        menu = {
            "Coffee": [
                {
                    "name": "Espresso",
                    "description": "Rich single-shot espresso with intense aroma.",
                    "price": 180,
                    "veg": True,
                    "signature": False,
                    "image": "espresso.avif",
                },
                {
                    "name": "Classic Cappuccino",
                    "description": "Fresh espresso with velvety steamed milk foam.",
                    "price": 220,
                    "veg": True,
                    "signature": True,
                    "image": "cappuccino.avif",
                },
                {
                    "name": "Café Latte",
                    "description": "Smooth espresso blended with creamy steamed milk.",
                    "price": 240,
                    "veg": True,
                    "signature": True,
                    "image": "cafe latte.avif",
                },
                {
                    "name": "Mocha",
                    "description": "Espresso with Belgian chocolate and steamed milk.",
                    "price": 260,
                    "veg": True,
                    "signature": True,
                    "image": "mocha.avif",
                },
                {
                    "name": "Americano",
                    "description": "Bold espresso finished with hot water.",
                    "price": 190,
                    "veg": True,
                    "signature": False,
                    "image": "americano.avif",
                },
            ],

            "Tea": [
                {
                    "name": "Masala Chai",
                    "description": "Traditional Indian tea brewed with aromatic spices.",
                    "price": 120,
                    "veg": True,
                    "signature": True,
                    "image": "masala-chai.avif",
                },
                {
                    "name": "Green Tea",
                    "description": "Refreshing premium green tea leaves.",
                    "price": 150,
                    "veg": True,
                    "signature": False,
                    "image": "green tea.avif",
                },
            ],

            "Cold Beverages": [
                {
                    "name": "Iced Coffee",
                    "description": "Chilled coffee served over ice.",
                    "price": 260,
                    "veg": True,
                    "signature": True,
                    "image": "cold coffee.avif",
                },
                {
                    "name": "Chocolate Milkshake",
                    "description": "Creamy chocolate shake topped with whipped cream.",
                    "price": 280,
                    "veg": True,
                    "signature": True,
                    "image": "Chocolate Milkshake.avif",
                },
                {
                    "name": "Virgin Mojito",
                    "description": "Mint, lime and soda for a refreshing cooler.",
                    "price": 220,
                    "veg": True,
                    "signature": True,
                    "image": "Virgin Mojito.avif",
                },
                {
                    "name": "Blue Lagoon",
                    "description": "Sweet citrus mocktail with blue curacao syrup.",
                    "price": 250,
                    "veg": True,
                    "signature": True,
                    "image": "Blue Lagoon juice.avif",
                },
            ],

            "Sandwiches": [
                {
                    "name": "Veg Club Sandwich",
                    "description": "Grilled sandwich layered with fresh vegetables.",
                    "price": 250,
                    "veg": True,
                    "signature": True,
                    "image": "Veg Club Sandwich.avif",
                },
            ],

            "Pizza": [
                {
                    "name": "Margherita Pizza",
                    "description": "Classic mozzarella and basil pizza.",
                    "price": 420,
                    "veg": True,
                    "signature": True,
                    "image": "Margherita Pizza.avif",
                },
                {
                    "name": "Farmhouse Pizza",
                    "description": "Loaded with fresh vegetables and cheese.",
                    "price": 480,
                    "veg": True,
                    "signature": False,
                    "image": "Farmhouse Pizza.avif",
                },
            ],

            "Pasta": [
                {
                    "name": "Creamy Alfredo Pasta",
                    "description": "Creamy white sauce pasta with herbs.",
                    "price": 360,
                    "veg": True,
                    "signature": True,
                    "image": "Creamy Alfredo Pasta.webp",
                },
                {
                    "name": "Arrabbiata Pasta",
                    "description": "Penne tossed in spicy tomato sauce.",
                    "price": 340,
                    "veg": True,
                    "signature": False,
                    "image": "Arrabbiata Pasta.webp",
                },
            ],

            "Burgers": [
                {
                    "name": "Crispy Veg Burger",
                    "description": "Crunchy vegetable patty with fresh lettuce.",
                    "price": 280,
                    "veg": True,
                    "signature": True,
                    "image": "Crispy Veg Burger.avif",
                },
            ],

            "Sides": [
                {
                    "name": "Peri Peri Fries",
                    "description": "Golden fries tossed in peri peri seasoning.",
                    "price": 180,
                    "veg": True,
                    "signature": False,
                    "image": "Peri Peri Fries.webp",
                },
            ],

            "Desserts": [
                {
                    "name": "New York Cheesecake",
                    "description": "Classic creamy baked cheesecake.",
                    "price": 320,
                    "veg": True,
                    "signature": True,
                    "image": "New York Cheesecake.webp",
                },
                {
                    "name": "Chocolate Brownie",
                    "description": "Warm brownie served with chocolate drizzle.",
                    "price": 240,
                    "veg": True,
                    "signature": True,
                    "image": "Chocolate Brownie.webp",
                },
                {
                    "name": "Belgian Waffle",
                    "description": "Fresh waffle topped with maple syrup.",
                    "price": 290,
                    "veg": True,
                    "signature": False,
                    "image": "Belgian Waffle.webp",
                },
            ],
        }

        for order, (category_name, items) in enumerate(menu.items(), start=1):

            category, _ = MenuCategory.objects.get_or_create(
                name=category_name,
                defaults={"order": order},
            )

            category.order = order
            category.save()

            self.stdout.write(self.style.SUCCESS(f"{category_name}"))

            for item in items:

                obj, created = MenuItem.objects.get_or_create(
                    category=category,
                    name=item["name"],
                    defaults={
                        "description": item["description"],
                        "price": item["price"],
                        "is_veg": item["veg"],
                        "is_signature": item["signature"],
                        "available": True,
                    },
                )

                # Update existing fields every time
                obj.description = item["description"]
                obj.price = item["price"]
                obj.is_veg = item["veg"]
                obj.is_signature = item["signature"]
                obj.available = True
                obj.save()

                # Upload/update image every time
                image_filename = item.get("image")
                if image_filename:
                    attach_image(obj, image_filename)

                if created:
                    self.stdout.write(f"   ✓ Added {obj.name}")
                else:
                    self.stdout.write(f"   ↻ Updated {obj.name}")

        self.stdout.write(
            self.style.SUCCESS("\nCopper Kettle menu seeded successfully!")
        )