from django.urls import path
from . import views

app_name = "cafe"

urlpatterns = [
    path("", views.home, name="home"),
    path("menu/", views.menu, name="menu"),
    path("gallery/", views.gallery, name="gallery"),
    path("reviews/", views.reviews, name="reviews"),
    path("reserve/", views.reserve, name="reserve"),
    path("contact/", views.contact, name="contact"),
    path("reservation/<int:pk>/whatsapp/", views.whatsapp_notify, name="whatsapp_notify"),
    path("cart/", views.cart_detail, name="cart"),
    path("cart/add/<int:item_id>/", views.cart_add, name="cart_add"),
    path("cart/remove/<int:item_id>/", views.cart_remove, name="cart_remove"),
    path("cart/increase/<int:item_id>/", views.cart_increase, name="cart_increase"),
    path("cart/decrease/<int:item_id>/", views.cart_decrease, name="cart_decrease"),
    path("cart/clear/", views.cart_clear, name="cart_clear"),
    path("checkout/", views.checkout, name="checkout"),
    path("order/<int:pk>/status/", views.order_status, name="order_status"),
    path("orders/", views.my_orders, name="my_orders"),
    path("order/<int:pk>/status.json/", views.order_status_json, name="order_status_json"),
    path("order/<int:pk>/pay/", views.payment, name="payment"),
    path("order/<int:pk>/pay/verify/", views.payment_verify, name="payment_verify"),
]

