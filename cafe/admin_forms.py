from django import forms
from .models import Reservation

class ReservationAdminForm(forms.ModelForm):

    class Meta:
        model = Reservation
        fields = "__all__"

        widgets = {
            "admin_message": forms.Textarea(
                attrs={
                    "rows": 5,
                    "cols": 60,
                    "placeholder": "Type message for customer..."
                }
            )
        }