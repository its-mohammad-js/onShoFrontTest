from rest_framework import serializers

from .models import Webinar, WebinarTopic


class WebinarListSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = Webinar
        fields = ['id', 'title', 'speaker', 'date', 'start_time', 'end_time', 'price', 'is_free', 'image']

    def get_image(self, obj):
        request = self.context.get('request')
        if obj.image:
            return request.build_absolute_uri(obj.image.url)
        return None


class WebinarTopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = WebinarTopic
        fields = ['title', 'content']


class WebinarDetailSerializer(serializers.ModelSerializer):
    topics = WebinarTopicSerializer(many=True, read_only=True)
    image = serializers.SerializerMethodField()

    class Meta:
        model = Webinar
        fields = ['id', 'title', 'description', 'speaker', 'date', 'start_time', 'end_time', 'price', 'is_free',
                  'image', 'topics']

    def get_image(self, obj):
        request = self.context.get('request')
        if obj.image:
            return request.build_absolute_uri(obj.image.url)
        return None
