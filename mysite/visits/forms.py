from django import forms
from .models import Goal


class GoalSelectionForm(forms.Form):
    goals = forms.ModelMultipleChoiceField(
        queryset=Goal.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        label="اختاري أهداف زيارتك",
        required=True,
        error_messages={
            "required": "اختاري هدفًا واحدًا على الأقل.",
        },
    )
