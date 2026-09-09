from django import forms
from .models import AskedQuestion


class AskedQuestionModelForm(forms.ModelForm):
    class Meta:
        model = AskedQuestion
        fields = ["question"]

        widgets = {
            "question": forms.Textarea(
                attrs={
                    "id" :"chatInput",
                    "class": "form-control chat-textarea",
                    "placeholder": "Message RAGKit...",
                    "rows": 1,
                    "maxlength": 2000,
                    "aria-label" : "Type your message",
                    "autocomplete" : "off"
                }
            )
        }