from django import forms
from .models import VisitorProfile


class VisitorProfileForm(forms.ModelForm):
    class Meta:
        model = VisitorProfile
        fields = [
            "available_minutes",
            "use_sign_language",
            "show_captions",
            "use_text_to_speech",
        ]
        widgets = {
            "available_minutes": forms.NumberInput(attrs={"min": 1}),
        }
