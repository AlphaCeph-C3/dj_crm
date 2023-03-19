from django import forms

from crm.models import Agent


class AgentModelForm(forms.ModelForm):
    class Meta:
        model = Agent
        fields = ("user",)
