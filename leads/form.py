from django.forms import ModelForm
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UsernameField
from .models import Lead

User = get_user_model()
class LeadForm(ModelForm):
    class Meta:
        model = Lead
        fields = [
            "first_name",
            "last_name",
            "age",
            "agent"
        ]

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username",)
        field_classes = {"username": UsernameField}