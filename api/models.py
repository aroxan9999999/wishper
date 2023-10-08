from django.db import models
from django.contrib.auth.models import AbstractUser
import secrets
from rest_framework.authtoken.models import Token


class CustomUser(AbstractUser):
    user_id_from_telegram = models.PositiveSmallIntegerField(unique=True, blank=True, null=True)

    def __str__(self):
        return self.username


class CustomToken(Token):
    user_id_from_telegram = models.PositiveSmallIntegerField(unique=True)


class Subscription(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    subscribed_at = models.DateTimeField(auto_now_add=True)
    telegram_token = models.CharField(max_length=255, unique=True, blank=True)

    def generate_unique_token(self):
        while True:
            token = secrets.token_hex(16)
            if not Subscription.objects.filter(telegram_token=token).exists():
                return token

    def save(self, *args, **kwargs):
        if not self.telegram_token:
            self.telegram_token = self.generate_unique_token()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} subscribed at {self.subscribed_at}"


class Message(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} - {self.timestamp}'
