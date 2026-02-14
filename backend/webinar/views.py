from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Webinar
from .serializers import WebinarListSerializer, WebinarDetailSerializer


class CustomPagination(PageNumberPagination):
    page_size = 6  # تعداد آیتم‌ها در هر صفحه
    page_size_query_param = 'page_size'
    max_page_size = 50


class WebinarListView(APIView):
    def post(self, request):
        webinars = Webinar.objects.all()
        paginator = CustomPagination()
        result_page = paginator.paginate_queryset(webinars, request)
        serializer = WebinarListSerializer(result_page, many=True, context={'request': request})

        response_data = {
            "status": True,
            "data": {
                "count": paginator.page.paginator.count,
                "next": paginator.get_next_link(),
                "previous": paginator.get_previous_link(),
                "results": serializer.data
            }
        }
        return Response(response_data)


class WebinarDetailView(APIView):
    def post(self, request):
        webinar_id = request.data.get('webinar_id')  # دریافت ID از بادی درخواست
        if not webinar_id:
            return Response({"status": False, "message": "شناسه وبینار ارسال نشده است"},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            webinar = Webinar.objects.get(id=webinar_id)
            serializer = WebinarDetailSerializer(webinar, context={'request': request})
            return Response({"status": True, "data": serializer.data}, status=status.HTTP_200_OK)
        except Webinar.DoesNotExist:
            return Response({"status": False, "message": "وبینار پیدا نشد"}, status=status.HTTP_404_NOT_FOUND)
