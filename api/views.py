from rest_framework.views import APIView
from .models import Subscription, Message, CustomUser, CustomToken
from .serializers import SubscriptionSerializer, MessageSerializer, UserSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated


@api_view(['POST'])
def register_user(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        user.set_password(serializer.validated_data['password'])
        user.save()
        user_id = serializer.validated_data['user_id_from_telegram']
        print(user_id)
        token, created = CustomToken.objects.get_or_create(user=user, user_id_from_telegram=user_id)
        return Response({'message': 'User registered successfully', 'token': token.key}, status=status.HTTP_201_CREATED)
    else:
        error_messages = serializer.errors
        error_field = list(error_messages.keys())[0] in ['username', 'user_id_from_telegram']
        if error_field:
            error_message = list(error_messages.values())[0][0]
            return Response({'message': error_message}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'message': 'invalid data'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def get_token(request):
    user_id = request.data.get('user_id')
    try:
        token = CustomToken.objects.get(user_id_from_telegram=user_id)
        return Response({"message": token.key}, status=200)
    except CustomToken.DoesNotExist:
        return Response({"message": f'No registered user with user_id {user_id}'}, status=400)


class SubscribeView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        existing_subscription = Subscription.objects.filter(user=user).exists()
        if existing_subscription:
            return Response({'message': 'Вы уже подписаны.'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = SubscriptionSerializer(data={'user': user.id})
        if serializer.is_valid():
            subscription = serializer.save()
            return Response({
                'message': f'Спасибо за подписку! Теперь вы подписаны на нашего бота, ваш толкен {subscription.telegram_token} .'},
                status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def get_user_messages(request):
    user = request.user
    messages = Message.objects.filter(user=user).order_by('-timestamp')
    serializer = MessageSerializer(messages, many=True)
    return Response(serializer.data, status=200)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def send_message(request):
    content = request.data.get("message")
    message = Message.objects.create(user=request.user, content=content)
    return Response({"message": content}, status=200)
