from django import forms
from .models import Reservation, ContactMessage, Review
from datetime import date, timedelta, time
from django.core.exceptions import ValidationError
import re
from .models import phone_validator


def generate_time_choices():
    choices = []
    slot = time(10, 0)
    while slot <= time(21, 0):
        label = slot.strftime("%I:%M %p").lstrip("0")
        value = slot.strftime("%H:%M")
        choices.append((value, label))
        minutes = slot.hour * 60 + slot.minute + 30
        if minutes > 21 * 60:
            break
        slot = time(minutes // 60, minutes % 60)
    return choices

TIME_CHOICES = generate_time_choices()


class ReservationForm(forms.ModelForm):

    class Meta:
        model = Reservation
        fields = ["name", "phone", "email", "party_size", "date", "time", "notes"]

        widgets = {
            "date": forms.DateInput(
                attrs={
                    "type": "date"
                }
            ),

            "phone": forms.TextInput(
                attrs={
                    "maxlength":10,
                    "pattern":"[0-9]{10}",
                    "placeholder":"9876543210"
                }
            ),

            "time": forms.Select(choices=TIME_CHOICES),
            
            "notes": forms.TextInput(
                attrs={
                    "placeholder": "Anything we should know? (optional)"
                }
            ),
        }

    def clean_phone(self):
        phone = self.cleaned_data["phone"]

        if not re.fullmatch(r"\d{10}", phone):
            raise ValidationError(
                "Phone number must contain exactly 10 digits."
            )

        return phone

    def clean_date(self):

        booking_date = self.cleaned_data["date"]

        today = date.today()

        max_date = today + timedelta(days=30)

        if booking_date < today:
            raise ValidationError(
                "Past dates are not allowed."
            )

        if booking_date > max_date:
            raise ValidationError(
                "Reservations are allowed only up to 30 days in advance."
            )

        return booking_date

    def clean_time(self):

        booking_time = self.cleaned_data["time"]

        if booking_time < time(10,0) or booking_time > time(21,0):
            raise ValidationError(
                "Reservation time must be between 10:00 AM and 9:00 PM."
            )

        return booking_time

class ContactForm(forms.ModelForm):

    class Meta:
        model = ContactMessage

        fields = [
            "name",
            "phone",
            "email",
            "subject",
            "message",
        ]

        widgets = {

            "name": forms.TextInput(attrs={
                "class":"form-control",
                "placeholder":"Your Name"
            }),

            "phone": forms.TextInput(attrs={
                "class":"form-control",
                "placeholder":"9876543210",
                "maxlength":"10",
                "pattern":"[0-9]{10}"
            }),

            "email": forms.EmailInput(attrs={
                "class":"form-control",
                "placeholder":"example@email.com"
            }),

            "subject": forms.TextInput(attrs={
                "class":"form-control",
                "placeholder":"Subject"
            }),

            "message": forms.Textarea(attrs={
                "class":"form-control",
                "rows":5,
                "placeholder":"Write your message..."
            }),

        }

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ["reviewer_name", "rating", "comment"]
        widgets = {
            "reviewer_name": forms.TextInput(attrs={"placeholder": "Your name"}),
            "rating": forms.HiddenInput(),
            "comment": forms.Textarea(attrs={"rows": 3, "placeholder": "Share your experience..."}),
        }

class CheckoutForm(forms.Form):
    ORDER_TYPE_CHOICES = [
        ("takeaway", "Takeaway"),
        ("delivery", "Delivery"),
    ]
    PAYMENT_CHOICES = [
        ("cash", "Cash / Pay at Restaurant"),
        ("online", "Pay Online"),
    ]

    customer_name = forms.CharField(max_length=100, label="Name")
    phone = forms.CharField(max_length=10, validators=[phone_validator])
    email = forms.EmailField(required=False)
    order_type = forms.ChoiceField(choices=ORDER_TYPE_CHOICES, widget=forms.RadioSelect)
    address = forms.CharField(widget=forms.Textarea(attrs={"rows": 2}), required=False)
    payment_method = forms.ChoiceField(choices=PAYMENT_CHOICES, widget=forms.RadioSelect)