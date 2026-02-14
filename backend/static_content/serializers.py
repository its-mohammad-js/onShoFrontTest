from rest_framework import serializers
from .models import StaticContent, RelatedLink


class RelatedLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = RelatedLink
        fields = ['title', 'description', 'url', 'external']


class StaticContentListSerializer(serializers.ModelSerializer):
    category = serializers.CharField(source='get_category_display', read_only=True)
    category_value = serializers.CharField(source='category', read_only=True)
    
    class Meta:
        model = StaticContent
        fields = ['id', 'title', 'short_description', 'slug', 'category', 'category_value', 'display_order', 'create_date', 'update_date']


class StaticContentDetailSerializer(serializers.ModelSerializer):
    related_links = RelatedLinkSerializer(many=True, read_only=True)
    category = serializers.CharField(source='get_category_display', read_only=True)
    category_value = serializers.CharField(source='category', read_only=True)

    class Meta:
        model = StaticContent
        fields = ['id', 'title', 'short_description', 'description', 'slug', 'category', 'category_value', 'display_order', 'related_links', 'create_date', 'update_date']

