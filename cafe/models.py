from django.db import models
from django.core.validators import RegexValidator
from decimal import Decimal

phone_validator = RegexValidator(
    regex=r'^\d{10}$',
    message='Phone number must be exactly 10 digits.'
)


class MenuCategory(models.Model):
    name = models.CharField(max_length=60)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "name"]
        verbose_name_plural = "Menu categories"

    def __str__(self):
        return self.name


class MenuItem(models.Model):
    category = models.ForeignKey(MenuCategory, related_name="items", on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=200, blank=True, help_text="Short sensory description, e.g. 'Steeped 18 hours, notes of cherry and cocoa'")
    price = models.DecimalField(max_digits=7, decimal_places=2)
    is_veg = models.BooleanField(default=True)
    is_signature = models.BooleanField(default=False, help_text="Shown on homepage as a signature item")
    image = models.ImageField(upload_to="menu/", blank=True, null=True)
    available = models.BooleanField(default=True)

    class Meta:
        ordering = ["category__order", "name"]

    def __str__(self):
        return f"{self.name} ({self.category.name})"


class GalleryImage(models.Model):
    caption = models.CharField(max_length=120, blank=True)
    image = models.ImageField(upload_to="gallery/")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return self.caption or f"Gallery image {self.pk}"

class Reservation(models.Model):

    STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("Confirmed", "Confirmed"),
        ("Rescheduled", "Rescheduled"),
        ("Cancelled", "Cancelled"),
    ]

    name = models.CharField(max_length=100)

    phone = models.CharField(
        max_length=10,
        validators=[phone_validator]
    )

    email = models.EmailField(blank=True)

    party_size = models.PositiveSmallIntegerField(default=2)

    date = models.DateField()

    time = models.TimeField()

    notes = models.CharField(max_length=200, blank=True)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="Pending"
    )

    admin_message = models.TextField(
        blank=True,
        help_text="Message to send to the customer."
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-date", "-time"]

    def __str__(self):
        return f"{self.name} — {self.date} {self.time} ({self.party_size})"

    

class Review(models.Model):
    RATING_CHOICES = [
        (1, "1 star"),
        (2, "2 stars"),
        (3, "3 stars"),
        (4, "4 stars"),
        (5, "5 stars"),
    ]

    reviewer_name = models.CharField(max_length=60)
    
    rating = models.PositiveSmallIntegerField(choices=RATING_CHOICES)
    comment = models.TextField(max_length=500)
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.reviewer_name} — {self.rating} stars"


class ContactMessage(models.Model):

    name = models.CharField(max_length=100)

    phone = models.CharField(
        max_length=10,
        validators=[phone_validator],
            blank=True,
            default=""

    )

    email = models.EmailField()

    subject = models.CharField(
        max_length=150,
        blank=True,
        default=""
    )

    message = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} - {self.subject}"


class Order(models.Model):

    ORDER_TYPES = [
        ("takeaway", "Takeaway"),
        ("delivery", "Delivery"),
    ]

    STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("Preparing", "Preparing"),
        ("Ready", "Ready"),
        ("Completed", "Completed"),
    ]

    customer_name = models.CharField(max_length=100)

    phone = models.CharField(
        max_length=10,
        validators=[phone_validator]
    )

    email = models.EmailField(blank=True)

    address = models.TextField(blank=True)

    order_type = models.CharField(
        max_length=20,
        choices=ORDER_TYPES,
        default="takeaway"
    )

    total_amount = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        default=0
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="Pending"
    )

    payment_id = models.CharField(
        max_length=200,
        blank=True
    )

    payment_method = models.CharField(
        max_length=10,
        choices=[("cash", "Cash / Pay at Restaurant"), ("online", "Pay Online")],
        default="cash"
    )

    ready_time = models.DateTimeField(null=True, blank=True, help_text="Expected pickup or delivery time")

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Order #{self.id}"


class OrderItem(models.Model):

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="items"
    )

    menu_item = models.ForeignKey(
        MenuItem,
        on_delete=models.CASCADE
    )

    quantity = models.PositiveIntegerField(default=1)

    price = models.DecimalField(
        max_digits=8,
        decimal_places=2
    )

    def subtotal(self):
        if self.price is None:
            return None
        return self.price * self.quantity