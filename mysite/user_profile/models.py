from tabnanny import verbose
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from PIL import Image


class Profile(models.Model):
    user = models.OneToOneField(
        get_user_model(),
        verbose_name=_('user'),
        on_delete=models.CASCADE,
        related_name='profile',
    )
    picture = models.ImageField(
        _("picture"),
        upload_to='user_profile/img/',
        default ='user_profile/img/default.png',
    )

    def __str__(self):
        return f'{str(self.user)} {_("profile")}'

    class Meta:
        verbose_name = _("user profile")
        verbose_name_plural = _("user profiles")
    
