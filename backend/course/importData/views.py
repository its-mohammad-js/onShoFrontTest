from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from course.services import CourseImportService


class CourseImportView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def post(self, request, *args, **kwargs):
        file = request.FILES.get("file")
        if not file:
            return Response({"error": "No file uploaded."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            result = CourseImportService.import_from_csv(file)
            return Response({
                "message": "Import finished.",
                "imported": result["imported"],
                "updated": result["updated"],
                "skipped": result["skipped"],
                "errors": result["errors"],
            }, status=status.HTTP_200_OK)

        except ValueError as e:
            # Missing headers, invalid format, etc.
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
