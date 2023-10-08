from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_user, name='register_user'),
    path('subscribe/', views.SubscribeView.as_view(), name='subscription'),
    path("send_message/", views.send_message, name='message'),
    path('messages_list/', views.get_user_messages, name='message_list'),
    path('get_token/', views.get_token, name='token'),
]
