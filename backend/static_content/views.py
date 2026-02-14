from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from .models import StaticContent
from .serializers import StaticContentListSerializer, StaticContentDetailSerializer


class StaticContentListView(APIView):
    """
    API endpoint to list all active static content items
    Results are ordered by category and display_order
    """
    def get(self, request, *args, **kwargs):
        queryset = StaticContent.objects.filter(is_active=True).order_by('category', 'display_order', '-create_date')
        serializer = StaticContentListSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class StaticContentDetailView(APIView):
    """
    API endpoint to get detail of a static content item by slug or id
    """
    def get(self, request, *args, **kwargs):
        slug = request.query_params.get('slug', None)
        content_id = request.query_params.get('id', None)

        if slug:
            content = get_object_or_404(StaticContent, slug=slug, is_active=True)
        elif content_id:
            content = get_object_or_404(StaticContent, id=content_id, is_active=True)
        else:
            return Response(
                {'error': 'Either slug or id parameter is required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = StaticContentDetailSerializer(content)
        return Response(serializer.data, status=status.HTTP_200_OK)
