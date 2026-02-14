from django.db import models
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from account.authentication import CustomJWTAuthentication
from course.models import Course
from .models import Chat, Message
from .serializers import ChatSerializer, MessageSerializer


class CreateChatAPI(APIView):
    authentication_classes = (CustomJWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        user = request.user
        title = request.data.get('title')
        content = request.data.get('content')
        course_id = request.data.get('course_id')

        if not title or not content:
            return Response({
                "status": False,
                "data": {"error": "Title and content are required."}
            }, status=status.HTTP_400_BAD_REQUEST)

        destination_user = None
        if course_id:
            try:
                course = Course.objects.get(id=course_id)
                destination_user = course.mentor  # Assuming `mentor` is a field in `Course`
            except Course.DoesNotExist:
                return Response({
                    "status": False,
                    "data": {"error": "Invalid course_id."}
                }, status=status.HTTP_400_BAD_REQUEST)

        chat = Chat.objects.create(
            title=title,
            source_user=user,
            destination_user=destination_user,
            course_id=course_id
        )

        Message.objects.create(
            chat=chat,
            user=user,
            content=content
        )

        return Response({
            "status": True,
            "data": {"message": "Chat created successfully.", "chat_id": chat.id}
        }, status=status.HTTP_201_CREATED)


class SendMessageAPI(APIView):
    authentication_classes = (CustomJWTAuthentication,)
    permission_classes = (IsAuthenticated,)
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        user = request.user
        chat_id = request.data.get('chat_id')
        content = request.data.get('content')
        file = request.FILES.get('file')

        if not chat_id or not content:
            return Response({
                "status": False,
                "data": {"error": "Chat ID and content are required."}
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            chat = Chat.objects.get(id=chat_id)
        except Chat.DoesNotExist:
            return Response({
                "status": False,
                "data": {"error": "Chat not found."}
            }, status=status.HTTP_404_NOT_FOUND)

        message = Message.objects.create(
            chat=chat,
            user=user,
            content=content,
            file=file
        )

        return Response({
            "status": True,
            "data": {"message": "Message sent successfully.", "message_id": message.id}
        }, status=status.HTTP_201_CREATED)


class ChatListView(APIView):
    authentication_classes = (CustomJWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        user = request.user
        chats = Chat.objects.filter(models.Q(source_user=user) | models.Q(destination_user=user))
        serializer = ChatSerializer(chats, many=True)

        return Response({
            "status": True,
            "data": serializer.data
        }, status=status.HTTP_200_OK)


class ChatDetailView(APIView):
    authentication_classes = (CustomJWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        user = request.user
        chat_id = request.data.get('chat_id')

        if not chat_id:
            return Response({
                "status": False,
                "data": {"error": "Chat ID is required."}
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            chat = Chat.objects.get(id=chat_id)
        except Chat.DoesNotExist:
            return Response({
                "status": False,
                "data": {"error": "Chat not found."}
            }, status=status.HTTP_404_NOT_FOUND)

        if chat.source_user != user and chat.destination_user != user:
            return Response({
                "status": False,
                "data": {"error": "You do not have permission to view this chat."}
            }, status=status.HTTP_403_FORBIDDEN)

        chat_data = ChatSerializer(chat).data
        messages = chat.messages.all().order_by('create_date')
        messages_data = MessageSerializer(messages, many=True, context={'request': request}).data

        return Response({
            "status": True,
            "data": {
                "chat": chat_data,
                "messages": messages_data
            }
        }, status=status.HTTP_200_OK)
