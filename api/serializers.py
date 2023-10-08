from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Subscription, CustomUser
from .models import Message


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = '__all__'


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'content', 'timestamp']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'password', 'first_name', 'user_id_from_telegram']
        extra_kwargs = {'password': {'write_only': True}}

        def validate_username(self, value):
            if CustomUser.objects.filter(username=value).exists():
                raise serializers.ValidationError(
                    {"error_field": "username", "error_message": "Пользователь с таким именем уже существует."})
            return value

        def validate_user_id_from_telegram(self, value):
            if CustomUser.objects.filter(user_id_from_telegram=value).exists():
                raise serializers.ValidationError({"error_field": "user_id_from_telegram",
                                                   "error_message": "Вы уже зарегестрированы!"})
            return value



