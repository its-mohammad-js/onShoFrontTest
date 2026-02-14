from rest_framework import serializers

from .models import Chat, Message


class MessageSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.username', read_only=True)
    file = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = ['id', 'user', 'content', 'file', 'create_date', 'update_date']

    def get_file(self, obj):
        request = self.context.get('request')
        if obj.file and request:
            return request.build_absolute_uri(obj.file.url)
        return None


class ChatSerializer(serializers.ModelSerializer):
    source_user = serializers.CharField(source='source_user.username', read_only=True)
    destination_user = serializers.CharField(source='destination_user.username', read_only=True)
    course = serializers.CharField(source='course.title', read_only=True)

    class Meta:
        model = Chat
        fields = ['id', 'title', 'source_user', 'destination_user', 'course', 'create_date', 'update_date']
