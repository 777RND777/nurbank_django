from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.text import slugify


class User(AbstractUser):
    slug = models.SlugField(max_length=150, default="admin")
    debt = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.username)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.username

    class Meta:
        ordering = ["-pk"]
