from django.forms import ModelForm
from .models import Lead

class LeadForm(ModelForm):
    class Meta:
        model = Lead
        fields = [
            "first_name",
            "last_name",
            "age",
            "agent"
        ]