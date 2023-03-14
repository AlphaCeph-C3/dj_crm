from django.db import models
from django.utils.translation import gettext_lazy as _


class Lead(models.Model):
    first_name = models.CharField(_("First_Name"), max_length=20)
    last_name = models.CharField(_("Last_Name"), max_length=20)
    age = models.IntegerField(_("Age"), default=0)
    agent = models.ForeignKey(
        "Agent", on_delete=models.CASCADE, verbose_name=_("Agent Assigned")
    )


class Agent(models.Model):
    first_name = models.CharField(_("First_Name"), max_length=20)
    last_name = models.CharField(_("Last_Name"), max_length=20)
