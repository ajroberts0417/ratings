from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    """Default user for Rate Everything."""

    #: First and last name do not cover name patterns around the globe
    name = models.CharField(_("Name of User"), blank=True, max_length=255)

    def get_absolute_url(self):
        """Get url for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"username": self.username})


class DiscordUser(models.Model):
    """A model tying a user to a specific discord id."""

    user = models.OneToOneField(
        User,
        related_name="discord_user",
        verbose_name=_("Related User"),
        on_delete=models.CASCADE,
    )
    discord_id = models.CharField(unique=True, max_length=50, db_index=True)
