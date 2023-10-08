from django.contrib import admin
from .models import CustomUser, Subscription, Message


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'user_id_from_telegram', 'first_name')


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'subscribed_at', 'telegram_token')


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('user', 'content', 'timestamp')
