from django.contrib import messages
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from .models import (
    MenuCategory,
    MenuItem,
    GalleryImage,
    Reservation,
    Review,
)
from .forms import ReservationForm, ContactForm, ReviewForm
from django.shortcuts import get_object_or_404, redirect
from urllib.parse import quote
from .cart import Cart
from django.http import JsonResponse
from datetime import timedelta
from django.utils import timezone
from .models import Order, OrderItem
from .forms import CheckoutForm
import razorpay
from django.conf import settings
import json
import hmac
import hashlib
from django.views.decorators.csrf import csrf_exempt


def home(request):
    signature_items = MenuItem.objects.filter(is_signature=True, available=True)[:4]
    gallery_preview = GalleryImage.objects.all()[:3]
    top_reviews = Review.objects.filter(is_approved=True).order_by("-rating", "-created_at")[:3]
    return render(request, "cafe/home.html", {
        "signature_items": signature_items,
        "gallery_preview": gallery_preview,
        "top_reviews": top_reviews,
    })

def menu(request):
    categories = MenuCategory.objects.prefetch_related("items").all()
    return render(request, "cafe/menu.html", {"categories": categories})


def gallery(request):
    images = GalleryImage.objects.all()
    return render(request, "cafe/gallery.html", {"images": images})


def reserve(request):
    if request.method == "POST":
        form = ReservationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your table is requested — we'll confirm shortly by phone.")
            return redirect("cafe:reserve")
    else:
        form = ReservationForm()
    return render(request, "cafe/reserve.html", {"form": form})

def whatsapp_notify(request, pk):
    reservation = get_object_or_404(Reservation, pk=pk)

    phone = "91" + reservation.phone

    if reservation.status == "Confirmed":
        status_message = (
            "🎉 Great news! Your reservation has been confirmed.\n\n"
            "We look forward to serving you."
        )

    elif reservation.status == "Rescheduled":
        status_message = (
            "Unfortunately your requested slot is unavailable.\n\n"
            f"{reservation.admin_message}"
        )

    elif reservation.status == "Cancelled":
        status_message = (
            "We regret to inform you that your reservation has been cancelled.\n\n"
            f"{reservation.admin_message}"
        )

    else:
        status_message = (
            "Your reservation request is currently under review."
        )

        message = f"""
            Hello {reservation.name},

            ☕ *Copper Kettle Café*

            Reservation Details

            📅 Date: {reservation.date}
            🕒 Time: {reservation.time}
            👥 Guests: {reservation.party_size}

            Status: {reservation.status}

            {status_message}

            Thank you for choosing Copper Kettle Café.
            """

        whatsapp_url = f"https://wa.me/{phone}?text={quote(message)}"

        return redirect(whatsapp_url)


def reviews(request):
    approved_reviews = Review.objects.filter(is_approved=True)

    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Thanks for your review — it'll appear once approved.")
            return redirect("cafe:reviews")
    else:
        form = ReviewForm()

    return render(request, "cafe/reviews.html", {
        "reviews": approved_reviews,
        "form": form,
    })


def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Message sent — we'll get back to you soon.")
            return redirect("cafe:contact")
    else:
        form = ContactForm()
    return render(request, "cafe/contact.html", {"form": form})

def cart_detail(request):

    cart = Cart(request)

    return render(request, "cart/cart.html", {
        "cart": cart
    })



def cart_add(request, item_id):

    item = get_object_or_404(MenuItem, id=item_id)

    if not item.available:
        return JsonResponse({
            "success": False,
            "message": "This item is currently unavailable."
        })

    cart = Cart(request)
    cart.add(item)

    total_items = len(cart)

    return JsonResponse({
        "success": True,
        "message": f"{item.name} added to cart.",
        "count": total_items
    })


def cart_clear(request):

    cart = Cart(request)

    cart.clear()

    return JsonResponse({
        "success": True
    })


def cart_increase(request, item_id):

    cart = Cart(request)

    item = get_object_or_404(MenuItem, id=item_id)

    cart.add(item)

    data = cart.get_item_data(item.id)

    return JsonResponse(data)


def cart_decrease(request, item_id):

    cart = Cart(request)

    item = get_object_or_404(MenuItem, id=item_id)

    cart.decrease(item)

    data = cart.get_item_data(item.id)

    return JsonResponse(data)


def cart_remove(request, item_id):

    cart = Cart(request)

    item = get_object_or_404(MenuItem, id=item_id)

    cart.remove(item)

    return JsonResponse({
        "removed": True,
        "count": len(cart),
        "grand_total": cart.get_total_price()
    })

def checkout(request):
    cart = Cart(request)

    if len(cart) == 0:
        messages.error(request, "Your cart is empty.")
        return redirect("cafe:menu")

    initial = {
        "customer_name": request.COOKIES.get("ck_name", ""),
        "phone": request.COOKIES.get("ck_phone", ""),
        "email": request.COOKIES.get("ck_email", ""),
    }

    if request.method == "POST":
        form = CheckoutForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data

            estimate_minutes = 40 if data["order_type"] == "delivery" else 20

            order = Order.objects.create(
                customer_name=data["customer_name"],
                phone=data["phone"],
                email=data["email"],
                address=data["address"],
                order_type=data["order_type"],
                payment_method=data["payment_method"],
                total_amount=cart.get_total_price(),
                ready_time=timezone.now() + timedelta(minutes=estimate_minutes),
            )

            for cart_item in cart:
                # Skip items with missing or invalid prices (corrupted cart data)
                if cart_item.get("price") is None or cart_item.get("item") is None:
                    continue
                
                OrderItem.objects.create(
                    order=order,
                    menu_item=cart_item["item"],
                    quantity=cart_item["quantity"],
                    price=cart_item["price"],
                )

            cart.clear()

            existing_ids = request.COOKIES.get("ck_orders", "")
            id_list = [i for i in existing_ids.split(",") if i]
            id_list.append(str(order.pk))
            id_list = id_list[-20:]  # keep only the most recent 20
            if data["payment_method"] == "online":
                response = redirect("cafe:payment", pk=order.pk)
            else:
                response = redirect("cafe:order_status", pk=order.pk)
            response.set_cookie("ck_name", data["customer_name"], max_age=60 * 60 * 24 * 90)
            response.set_cookie("ck_phone", data["phone"], max_age=60 * 60 * 24 * 90)
            response.set_cookie("ck_email", data["email"], max_age=60 * 60 * 24 * 90)
            return response
    else:
        form = CheckoutForm(initial=initial)

    return render(request, "cafe/checkout.html", {
        "form": form,
        "cart": cart,
    })


def order_status(request, pk):
    order = get_object_or_404(Order, pk=pk)
    return render(request, "cafe/order_status.html", {"order": order})

def my_orders(request):
    cookie_ids = request.COOKIES.get("ck_orders", "")
    id_list = [i for i in cookie_ids.split(",") if i]

    remembered_orders = Order.objects.filter(pk__in=id_list)

    looked_up_orders = None
    phone_query = request.GET.get("phone", "").strip()

    if phone_query:
        looked_up_orders = Order.objects.filter(phone=phone_query)

    return render(request, "cafe/my_orders.html", {
        "remembered_orders": remembered_orders,
        "looked_up_orders": looked_up_orders,
        "phone_query": phone_query,
    })

def order_status_json(request, pk):
    order = get_object_or_404(Order, pk=pk)
    return JsonResponse({
        "status": order.status,
        "status_display": order.get_status_display(),
    })

def payment(request, pk):
    order = get_object_or_404(Order, pk=pk)

    client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

    amount_paise = int(order.total_amount * 100)  # Razorpay expects the smallest currency unit (paise)

    razorpay_order = client.order.create({
        "amount": amount_paise,
        "currency": "INR",
        "payment_capture": 1,
    })

    order.payment_id = razorpay_order["id"]
    order.save()

    return render(request, "cafe/payment.html", {
        "order": order,
        "razorpay_key_id": settings.RAZORPAY_KEY_ID,
        "razorpay_order_id": razorpay_order["id"],
        "amount_paise": amount_paise,
    })


def payment_verify(request, pk):
    order = get_object_or_404(Order, pk=pk)
    data = json.loads(request.body)

    payment_id = data.get("razorpay_payment_id", "")
    razorpay_order_id = data.get("razorpay_order_id", "")
    signature = data.get("razorpay_signature", "")

    generated_signature = hmac.new(
        key=settings.RAZORPAY_KEY_SECRET.encode(),
        msg=f"{razorpay_order_id}|{payment_id}".encode(),
        digestmod=hashlib.sha256
    ).hexdigest()

    if hmac.compare_digest(generated_signature, signature):
        order.payment_id = payment_id
        order.status = "Preparing"
        order.save()

        return JsonResponse({
            "success": True,
            "redirect_url": redirect("cafe:order_status", pk=order.pk).url
        })

    return JsonResponse({"success": False})