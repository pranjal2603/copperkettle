from django.contrib import admin
from .models import Reservation
from .models import MenuCategory, MenuItem, GalleryImage, Reservation, ContactMessage, Review, Order, OrderItem
from django.utils.html import format_html
from django.urls import reverse
from .admin_forms import ReservationAdminForm
from django.utils.html import format_html

@admin.register(MenuCategory)
class MenuCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "order")
    ordering = ("order",)


@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):

    list_display = (
        "image_preview",
        "name",
        "category",
        "price",
        "is_veg",
        "is_signature",
        "available",
    )

    list_filter = (
        "category",
        "is_veg",
        "is_signature",
        "available",
    )

    search_fields = (
        "name",
        "description",
    )

    ordering = (
        "category__order",
        "name",
    )

    list_editable = (
        "price",
        "is_signature",
        "available",
    )

    list_per_page = 20

    readonly_fields = ("image_preview_large",)

    fieldsets = (
        ("Basic Information", {
            "fields": (
                "category",
                "name",
                "description",
                "price",
            )
        }),

        ("Image", {
            "fields": (
                "image",
                "image_preview_large",
            )
        }),

        ("Options", {
            "fields": (
                "is_veg",
                "is_signature",
                "available",
            )
        }),
    )

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" width="60" height="60" '
                'style="border-radius:8px; object-fit:cover;" />',
                obj.image.url
            )
        return "—"

    image_preview.short_description = "Image"

    def image_preview_large(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" width="220" '
                'style="border-radius:10px;" />',
                obj.image.url
            )
        return "No image"

    image_preview_large.short_description = "Preview"


@admin.register(GalleryImage)
class GalleryImageAdmin(admin.ModelAdmin):
    list_display = ("caption", "order")
    ordering = ("order",)


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):

    form = ReservationAdminForm

    list_display = (
        "name",
        "phone",
        "date",
        "time",
        "party_size",
        "status",
    )

    list_filter = (
        "status",
        "date",
    )

    search_fields = (
        "name",
        "phone",
    )

    readonly_fields = (
        "whatsapp_link",
    )

    fieldsets = (

        ("Customer Details", {
            "fields": (
                "name",
                "phone",
                "email",
                "party_size",
            )
        }),

        ("Reservation", {
            "fields": (
                "date",
                "time",
                "notes",
                "status",
            )
        }),

        ("Customer Notification", {
            "fields": (
                "admin_message",
                "whatsapp_link",
            )
        }),

    )

    def whatsapp_link(self, obj):

        if not obj.pk:
            return "Save reservation first."

        url = reverse("cafe:whatsapp_notify", args=[obj.pk])

        return format_html(
            """
            <a href="{}"
               target="_blank"
               style="
               background:#25D366;
               color:white;
               padding:12px 18px;
               border-radius:8px;
               font-size:16px;
               text-decoration:none;
               font-weight:bold;
               ">
               💚 Send WhatsApp Notification
            </a>
            """,
            url,
        )

    whatsapp_link.short_description = ""

    
@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "created_at")
    readonly_fields = ("created_at",)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("reviewer_name", "rating", "is_approved", "created_at")
    list_filter = ("is_approved", "rating")
    list_editable = ("is_approved",)


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ("menu_item", "quantity", "price", "subtotal")

    def subtotal(self, obj):
        return obj.subtotal()


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "customer_name",
        "phone",
        "order_type",
        "status",
        "payment_method",
        "total_amount",
        "ready_time",
        "created_at",
    )

    list_filter = (
        "status",
        "order_type",
        "payment_method",
    )

    search_fields = (
        "customer_name",
        "phone",
        "email",
    )

    list_editable = (
        "status",
    )

    ordering = ("-created_at",)

    readonly_fields = ("customer_name", "phone", "email", "address", "order_type", "payment_method", "total_amount", "ready_time", "created_at")

    inlines = [OrderItemInline]