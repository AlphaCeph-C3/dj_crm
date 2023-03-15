from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    pass


class Lead(models.Model):
    first_name = models.CharField(_("First Name"), max_length=20)
    last_name = models.CharField(_("Last Name"), max_length=20)
    age = models.IntegerField(_("Age"), default=0)
    agent = models.ForeignKey(
        "Agent", on_delete=models.CASCADE, verbose_name=_("Agent Assigned")
    )

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"


class Agent(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, verbose_name=_("User Agent")
    )

    def __str__(self) -> str:
        return self.user.email
