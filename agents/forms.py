from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()


class AgentModelForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("username", "email", "first_name", "last_name")
