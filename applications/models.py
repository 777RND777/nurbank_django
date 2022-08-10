from django.contrib.auth.models import AbstractUser
from django.db import models

from users.models import User


class Application(models.Model):
    value = models.IntegerField()
    request_date = models.DateTimeField(auto_now_add=True)
    answer_date = models.DateTimeField(blank=True, null=True)
    approved = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="applications", null=True)

    def __str__(self):
        return str(self.id)

    class Meta:
        ordering = ["-pk"]
