from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    is_organizer = models.BooleanField(
        verbose_name="Organizer",
        default=True,
        help_text="Designates whether the user is a Organizer",
    )
    is_agent = models.BooleanField(
        verbose_name="Agent",
        default=False,
        help_text="Designates whether the user is a Agent",
    )


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class Lead(models.Model):
    first_name = models.CharField(_("First Name"), max_length=20)
    last_name = models.CharField(_("Last Name"), max_length=20)
    age = models.IntegerField(_("Age"), default=0)
    organization = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    agent = models.ForeignKey(
        "Agent",
        on_delete=models.SET_NULL,
        verbose_name=_("Agent Assigned"),
        null=True,
        blank=True,
    )

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"


class Agent(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, verbose_name=_("User Agent")
    )
    organization = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.user.first_name
