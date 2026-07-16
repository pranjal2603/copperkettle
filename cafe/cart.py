from decimal import Decimal
from .models import MenuItem


class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get("cart")

        if not cart:
            cart = self.session["cart"] = {}

        self.cart = cart

    def add(self, item, quantity=1):

        item_id = str(item.id)

        if item_id not in self.cart:

            self.cart[item_id] = {
                "quantity": 0,
                "price": str(item.price)
            }

        self.cart[item_id]["quantity"] += quantity

        self.save()

    def save(self):
        self.session.modified = True

    def remove(self, item):

        item_id = str(item.id)

        if item_id in self.cart:
            del self.cart[item_id]
            self.save()

    def decrease(self, item):

        item_id = str(item.id)

        if item_id in self.cart:

            self.cart[item_id]["quantity"] -= 1

            if self.cart[item_id]["quantity"] <= 0:
                del self.cart[item_id]

            self.save()

    def clear(self):

        self.session["cart"] = {}

        self.save()

    def __iter__(self):

        ids = self.cart.keys()

        items = MenuItem.objects.filter(id__in=ids)

        cart = self.cart.copy()

        for item in items:

            cart[str(item.id)]["item"] = item

        for value in cart.values():

            value["price"] = Decimal(value["price"])

            value["total"] = value["price"] * value["quantity"]

            yield value

    def __len__(self):

        return sum(item["quantity"] for item in self.cart.values())

    def get_total_price(self):
        return sum(
            Decimal(item["price"]) * item["quantity"]
            for item in self.cart.values()
        )

    def __bool__(self):
        return len(self) > 0