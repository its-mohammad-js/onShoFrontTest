import json
from datetime import datetime

from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from account.authentication import CustomJWTAuthentication
from account.models import OrganizerTeacher, Organizer, User
from . import models
from .serializers import CourseListSerializer, CourseSerializer, TeacherCourseSerializer, PublicCourseSerializer, RecursiveCategorySerializer, CategorySerializer, CommentCreateSerializer, \
    CreateRemoveWishListSerializer, TaskSerializer, CreateOrganizerSerializer, \
    CourseCreateSerializer, \
    ChapterCreateSerializer, LessonCreateSerializer, LessonUpdateSerializer, CourseUserSerializer, \
    AttributeListSerializer, OrganizationListSerializer, TaskAnswerSerializer, TaskDetailSerializer, \
    AnswerListSerializer, StandardsSerializer, RecursiveStandardsSerializer, StandardsListSerializer, \
    StandardsCreateUpdateSerializer, StandardsDetailSerializer


class CoursePagination(PageNumberPagination):
    page_size = 10  # تعداد نتایج در هر صفحه
    page_size_query_param = 'page_size'
    max_page_size = 100  # حداکثر تعداد نتایج در هر صفحه


class CourseListView(APIView):
    def post(self, request, *args, **kwargs):
        search_query = request.data.get('search', None)
        ordering = request.data.get('ordering', '-create_date')
        category_id = request.data.get('category_id', None)
        organizer_id = request.data.get('organizer_id', None)
        min_price = request.data.get('min_price', None)
        max_price = request.data.get('max_price', None)
        course_type = request.data.get('type', None)  # Filter by course type
        page = request.data.get('page', 1)
        page_size = request.data.get('page_size', 10)

        # فقط دوره‌های تایید شده و منتشر شده را نمایش بده
        courses = models.Course.objects.filter(
            is_published=True,
            is_verified=True
        )

        if category_id:
            courses = courses.filter(category_id=category_id)

        if organizer_id:
            courses = courses.filter(organizer_id=organizer_id)

        if min_price:
            courses = courses.filter(price__gte=min_price)

        if max_price:
            courses = courses.filter(price__lte=max_price)

        if search_query:
            courses = courses.filter(title__icontains=search_query)

        # Filter by course type if provided
        if course_type:
            # Validate course_type value
            valid_types = ['offline', 'online', 'pre_registration']
            if course_type in valid_types:
                courses = courses.filter(type=course_type)

        if ordering:
            courses = courses.order_by(ordering)

        # Manual pagination since we're using POST with body parameters
        total_count = courses.count()
        start_index = (page - 1) * page_size
        end_index = start_index + page_size
        paginated_courses = courses[start_index:end_index]

        serializer = CourseListSerializer(paginated_courses, many=True, context={'request': request})

        # Calculate next and previous page URLs
        next_page = None
        previous_page = None
        
        if end_index < total_count:
            next_page = f"?page={page + 1}&page_size={page_size}"
        
        if page > 1:
            previous_page = f"?page={page - 1}&page_size={page_size}"

        response_data = {
            "status": True,
            "data": {
                "count": total_count,
                "next": next_page,
                "previous": previous_page,
                "data": serializer.data
            }
        }

        return Response(response_data, status=status.HTTP_200_OK)


class CourseDetailView(APIView):
    def post(self, request, *args, **kwargs):
        # دریافت slug یا id از داده‌های ارسال شده
        slug = request.data.get('slug')
        course_id = request.data.get('id')
        
        if not slug and not course_id:
            return Response(
                {
                    "status": False,
                    "data": {"error": "Slug or id is required."}
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            course = None
            
            # If id is explicitly provided, use it
            if course_id:
                course = models.Course.objects.get(id=course_id)
            # If slug is provided
            elif slug:
                # If slug looks like a number, try ID first as fallback
                if slug.isdigit():
                    try:
                        course = models.Course.objects.get(id=int(slug))
                    except models.Course.DoesNotExist:
                        # Try slug lookup if ID fails
                        course = models.Course.objects.get(slug=slug)
                else:
                    # Normal slug lookup
                    course = models.Course.objects.get(slug=slug)
                    
        except models.Course.DoesNotExist:
            return Response(
                {
                    "status": False,
                    "data": {"error": "Course not found."}
                },
                status=status.HTTP_404_NOT_FOUND
            )
        except ValueError:
            return Response(
                {
                    "status": False,
                    "data": {"error": "Invalid id format."}
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # بررسی اینکه دوره تایید شده و منتشر شده است
        # یا کاربر صاحب دوره است (برای مشاهده دوره‌های خودش)
        user = getattr(request, 'user', None)
        is_owner = False
        
        if user and user.is_authenticated:
            # بررسی اینکه آیا کاربر صاحب دوره است
            is_owner = (course.user == user or 
                       (hasattr(user, 'organizer') and user.organizer == course.organizer))
        
        # اگر دوره تایید نشده یا منتشر نشده و کاربر صاحب نیست، خطا بده
        if not course.is_published or not course.is_verified:
            if not is_owner:
                return Response(
                    {
                        "status": False,
                        "data": {"error": "Course is not available."}
                    },
                    status=status.HTTP_404_NOT_FOUND
                )

        serializer = PublicCourseSerializer(course, context={'request': request})
        return Response(
            {
                "status": True,
                "data": serializer.data
            },
            status=status.HTTP_200_OK
        )


class CategoryListView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            category_id = request.data.get('category_id', None)

            # یکبار همه دسته‌بندی‌ها را می‌خوانیم (فقط فیلدهای لازم)
            all_categories = list(models.Category.objects.only(
                'id', 'title', 'slug', 'logo', 'parent_id', 'home_page'
            ))

            # ساخت دیکشنری برای دسترسی سریع
            cat_dict = {c.id: c for c in all_categories}

            # ساخت children برای هر دسته‌بندی در حافظه
            children_map = {}
            roots = []
            for c in all_categories:
                children_map.setdefault(c.id, [])
                if c.parent_id:
                    children_map.setdefault(c.parent_id, []).append(c)
                else:
                    roots.append(c)

            def build_tree(cat):
                logo_url = None
                if cat.logo:
                    logo_url = request.build_absolute_uri(cat.logo.url)
                children = children_map.get(cat.id, [])
                return {
                    'id': cat.id,
                    'title': cat.title,
                    'logo': logo_url,
                    'slug': cat.slug,
                    'home_page': cat.home_page,
                    'children': [build_tree(child) for child in children] if children else None
                }

            if category_id:
                # برگرداندن یک کتگوری خاص و فرزندانش
                category = cat_dict.get(int(category_id))
                if not category:
                    return Response({
                        "status": False,
                        "data": {"error": "Category not found."}
                    }, status=status.HTTP_404_NOT_FOUND)

                return Response({
                    "status": True,
                    "data": build_tree(category)
                }, status=status.HTTP_200_OK)
            else:
                # برگرداندن همه کتگوری‌ها و فرزندانشان
                return Response({
                    "status": True,
                    "data": [build_tree(root) for root in roots]
                }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                "status": False,
                "data": {"error": str(e)}
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class HomePageCategoryListView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            # Get all categories with home_page=True
            # Order by display_order (ascending - lower number = higher priority)
            # If display_order is null, treat it as 9999 (lowest priority)
            from django.db.models import F, Case, When, IntegerField
            categories = models.Category.objects.filter(home_page=True).annotate(
                order_value=Case(
                    When(display_order__isnull=True, then=9999),
                    default=F('display_order'),
                    output_field=IntegerField()
                )
            ).order_by('order_value', '-create_date')
            
            serializer = CategorySerializer(categories, many=True, context={'request': request})
            return Response({
                "status": True,
                "data": serializer.data
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                "status": False,
                "data": {"error": str(e)}
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def get_all_category_ids(category):
    """
    Recursively get all category IDs including the category itself and all its descendants.
    Returns a list of category IDs.
    """
    category_ids = [category.id]
    
    def get_children(cat):
        children = models.Category.objects.filter(parent=cat)
        for child in children:
            category_ids.append(child.id)
            get_children(child)  # Recursively get grandchildren
    
    get_children(category)
    return category_ids


class TrendingCoursesView(APIView):
    """Get trending courses filtered by category (including subcategories). category_id is required."""
    
    def post(self, request, *args, **kwargs):
        try:
            category_id = request.data.get('category_id', None)
            page = request.data.get('page', 1)
            page_size = request.data.get('page_size', 10)
            
            # Return empty results if category_id is not provided
            if not category_id:
                return Response({
                    "status": True,
                    "data": {
                        "count": 0,
                        "next": None,
                        "previous": None,
                        "page": page,
                        "page_size": page_size,
                        "results": []
                    }
                }, status=status.HTTP_200_OK)
            
            # Get trending courses filtered by category
            try:
                category = models.Category.objects.get(id=category_id)
                # Get all category IDs including parent and all descendants
                category_ids = get_all_category_ids(category)
                courses = models.Course.objects.filter(
                    is_trending=True,
                    category_id__in=category_ids,
                    is_published=True,
                    is_verified=True
                ).order_by('-create_date')
            except models.Category.DoesNotExist:
                return Response({
                    "status": False,
                    "data": {"error": "Category not found."}
                }, status=status.HTTP_404_NOT_FOUND)
            
            # Manual pagination
            total_count = courses.count()
            start_index = (page - 1) * page_size
            end_index = start_index + page_size
            paginated_courses = courses[start_index:end_index]
            
            serializer = CourseListSerializer(paginated_courses, many=True, context={'request': request})
            
            # Calculate next and previous page
            next_page = None
            previous_page = None
            
            if end_index < total_count:
                next_page = page + 1
            
            if page > 1:
                previous_page = page - 1
            
            return Response({
                "status": True,
                "data": {
                    "count": total_count,
                    "next": next_page,
                    "previous": previous_page,
                    "page": page,
                    "page_size": page_size,
                    "results": serializer.data
                }
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({
                "status": False,
                "data": {"error": str(e)}
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class PopularCoursesView(APIView):
    """Get popular courses filtered by category (including subcategories). category_id is required."""
    
    def post(self, request, *args, **kwargs):
        try:
            category_id = request.data.get('category_id', None)
            page = request.data.get('page', 1)
            page_size = request.data.get('page_size', 10)
            
            # Return empty results if category_id is not provided
            if not category_id:
                return Response({
                    "status": True,
                    "data": {
                        "count": 0,
                        "next": None,
                        "previous": None,
                        "page": page,
                        "page_size": page_size,
                        "results": []
                    }
                }, status=status.HTTP_200_OK)
            
            # Get popular courses filtered by category
            try:
                category = models.Category.objects.get(id=category_id)
                # Get all category IDs including parent and all descendants
                category_ids = get_all_category_ids(category)
                courses = models.Course.objects.filter(
                    is_popular=True,
                    category_id__in=category_ids,
                    is_published=True,
                    is_verified=True
                ).order_by('-create_date')
            except models.Category.DoesNotExist:
                return Response({
                    "status": False,
                    "data": {"error": "Category not found."}
                }, status=status.HTTP_404_NOT_FOUND)
            
            # Manual pagination
            total_count = courses.count()
            start_index = (page - 1) * page_size
            end_index = start_index + page_size
            paginated_courses = courses[start_index:end_index]
            
            serializer = CourseListSerializer(paginated_courses, many=True, context={'request': request})
            
            # Calculate next and previous page
            next_page = None
            previous_page = None
            
            if end_index < total_count:
                next_page = page + 1
            
            if page > 1:
                previous_page = page - 1
            
            return Response({
                "status": True,
                "data": {
                    "count": total_count,
                    "next": next_page,
                    "previous": previous_page,
                    "page": page,
                    "page_size": page_size,
                    "results": serializer.data
                }
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({
                "status": False,
                "data": {"error": str(e)}
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class AddCommentRateView(APIView):
    authentication_classes = [CustomJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        data = request.data

        # Validate and save the comment
        comment_serializer = CommentCreateSerializer(data=data, context={'request': request})
        if comment_serializer.is_valid():
            comment = comment_serializer.save()

            # Check if 'rate' is provided in the request
            rate_value = data.get('rate')
            if rate_value is not None:
                # Ensure the rate is valid
                if not (1 <= int(rate_value) <= 5):
                    return Response({
                        'status': False,
                        'error': 'Rate must be between 1 and 5.'
                    }, status=status.HTTP_400_BAD_REQUEST)

                # Check if the user has already rated this course
                course = comment.course
                if models.Rate.objects.filter(user=user, course=course).exists():
                    return Response({
                        'status': False,
                        'error': 'You have already rated this course.'
                    }, status=status.HTTP_400_BAD_REQUEST)

                # Create a new rate record
                models.Rate.objects.create(user=user, course=course, rate=rate_value)

            return Response({
                'status': True,
                'data': comment_serializer.data,
            }, status=status.HTTP_201_CREATED)

        return Response(comment_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AttributeListView(APIView):
    authentication_classes = (CustomJWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        try:
            attributes = models.Attribute.objects.prefetch_related('values').all()
            serializer = AttributeListSerializer(attributes, many=True)
            return Response({
                "status": True,
                "data": serializer.data
            }, status=200)
        except Exception as e:
            return Response({
                "status": False,
                "message": str(e)
            }, status=500)


class CreateRemoveWishListView(APIView):
    authentication_classes = (CustomJWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        serializer = CreateRemoveWishListSerializer(data=request.data)

        # اعتبارسنجی داده‌ها
        if not serializer.is_valid():
            return Response({
                "status": False,
                "data": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

        course_id = serializer.validated_data.get('course_id')
        user = request.user
        course = models.Course.objects.get(id=course_id)

        # بررسی وجود نشان‌گذاری قبلی
        wishlist, created = models.WishList.objects.get_or_create(user=user, course=course)

        if not created:
            # اگر نشان‌گذاری قبلاً وجود داشت، حذفش کن
            wishlist.delete()
            return Response({
                "status": True,
                "data": {"message": "نشان‌گذاری با موفقیت حذف شد."}
            }, status=status.HTTP_200_OK)

        # اگر نشان‌گذاری ایجاد شد
        return Response({
            "status": True,
            "data": {"message": "نشان‌گذاری با موفقیت اضافه شد."}
        }, status=status.HTTP_201_CREATED)


class ListWishListView(APIView):
    authentication_classes = (CustomJWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        user = request.user
        # فیلتر کردن لیست علاقه‌مندی‌ها بر اساس کاربر
        wishlist = models.WishList.objects.filter(user=user).select_related('course')

        # فقط لیست دوره‌ها را استخراج کنید
        courses = [item.course for item in wishlist]

        # سریالایز کردن دوره‌ها
        data = CourseListSerializer(courses, many=True, context={'request': request}).data

        return Response({
            "status": True,
            "data": data
        }, status=status.HTTP_200_OK)


class CreateTaskView(APIView):
    authentication_classes = (CustomJWTAuthentication,)
    permission_classes = (IsAuthenticated,)  # کاربر باید لاگین کرده باشد

    def post(self, request, *args, **kwargs):
        user = request.user

        # بررسی اینکه کاربر منتور است
        if not user.has_permission("task_create"):
            return Response({
                "status": False,
                "data": "فقط کاربران منتور مجاز به ایجاد تسک هستند."
            }, status=status.HTTP_403_FORBIDDEN)

        # دریافت داده‌ها از بادی
        title = request.data.get("title")
        description = request.data.get("description")
        course_id = request.data.get("course_id")
        lesson_id = request.data.get("lesson_id")  # اختیاری است
        difficulty = request.data.get("difficulty", "beginner")
        time_limit = request.data.get("time_limit")  # اختیاری است
        file = request.FILES.get("file")
        slug = request.data.get("slug")

        # اگر course_id ارسال شده باشد، بررسی و بازیابی
        course = None
        if course_id:
            course = get_object_or_404(models.Course, id=course_id)

        # اگر lesson_id ارسال شده باشد، بررسی و بازیابی
        lesson = None
        if lesson_id:
            lesson = get_object_or_404(models.Lesson, id=lesson_id)

        # ایجاد تسک
        task = models.Task.objects.create(
            title=title,
            description=description,
            mentor=user,  # منتور از JWT دریافت می‌شود
            course=course,
            lesson=lesson,
            difficulty=difficulty,
            time_limit=time_limit,
            file=file,
            slug=slug,
        )

        # تبدیل تسک به داده‌های سریالایز شده
        serializer = TaskSerializer(task, context={'request': request})
        
        # ساختار پاسخ مطابق با مستندات
        response_data = serializer.data.copy()
        response_data['course_id'] = course.id if course else None
        response_data['lesson_id'] = lesson.id if lesson else None
        response_data['created_at'] = task.create_date.isoformat() if hasattr(task, 'create_date') and task.create_date else None
        
        return Response({
            "status": True,
            "message": "تمرین با موفقیت ایجاد شد",
            "data": response_data
        }, status=status.HTTP_201_CREATED)


class TaskCourseLessonView(APIView):
    """Get courses and lessons for task creation"""
    authentication_classes = (CustomJWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        user = request.user
        
        # Get courses where user is mentor
        courses = models.Course.objects.filter(mentor=user).order_by('-create_date')
        
        course_data = []
        for course in courses:
            lessons = course.lessons.all().order_by('id')
            course_data.append({
                'id': course.id,
                'title': course.title,
                'slug': course.slug,
                'lessons': [
                    {
                        'id': lesson.id,
                        'title': lesson.title,
                        'slug': lesson.slug,
                        'chapter': lesson.chapter.title if lesson.chapter else None
                    }
                    for lesson in lessons
                ]
            })
        
        return Response({
            "status": True,
            "data": course_data
        }, status=status.HTTP_200_OK)


class StudentTasksView(APIView):
    """Get tasks for enrolled courses for students"""
    authentication_classes = (CustomJWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        user = request.user
        
        # Get courses where user is enrolled (in_progress or completed)
        enrolled_courses = models.CourseUser.objects.filter(
            user=user, 
            status__in=['in_progress', 'completed']
        ).select_related('course')
        
        tasks_data = []
        for enrollment in enrolled_courses:
            course = enrollment.course
            # Get tasks for this course
            tasks = models.Task.objects.filter(course=course).order_by('-create_date')
            
            for task in tasks:
                # Check if user has submitted this task
                submission = models.TaskAnswer.objects.filter(
                    task=task, 
                    user=user
                ).first()
                
                tasks_data.append({
                    'id': task.id,
                    'title': task.title,
                    'description': task.description,
                    'difficulty': task.get_difficulty_display(),
                    'file': request.build_absolute_uri(task.file.url) if task.file else None,
                    'course': {
                        'id': course.id,
                        'title': course.title,
                        'slug': course.slug
                    },
                    'lesson': {
                        'id': task.lesson.id,
                        'title': task.lesson.title,
                        'slug': task.lesson.slug
                    } if task.lesson else None,
                    'submission': {
                        'id': submission.id,
                        'status': submission.status.title if submission.status else None,
                        'submitted_at': submission.create_date
                    } if submission else None,
                    'create_date': task.create_date
                })
        
        return Response({
            "status": True,
            "data": tasks_data
        }, status=status.HTTP_200_OK)


class LessonAccessCheckView(APIView):
    """Check if student can access a lesson based on task completion"""
    authentication_classes = (CustomJWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        user = request.user
        lesson_id = request.GET.get('lesson_id')
        
        if not lesson_id:
            return Response({
                "status": False,
                "message": "Lesson ID is required"
            }, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            lesson = models.Lesson.objects.get(id=lesson_id)
        except models.Lesson.DoesNotExist:
            return Response({
                "status": False,
                "message": "Lesson not found"
            }, status=status.HTTP_404_NOT_FOUND)
        
        # Check if user is enrolled in the course
        enrollment = models.CourseUser.objects.filter(
            user=user,
            course=lesson.course,
            status='enrolled'
        ).first()
        
        if not enrollment:
            return Response({
                "status": False,
                "message": "User not enrolled in this course",
                "can_access": False
            }, status=status.HTTP_403_FORBIDDEN)
        
        # Check if there are any tasks for previous lessons that need to be completed
        course_lessons = models.Lesson.objects.filter(
            course=lesson.course
        ).order_by('id')
        
        current_lesson_index = None
        for i, l in enumerate(course_lessons):
            if l.id == lesson.id:
                current_lesson_index = i
                break
        
        if current_lesson_index is None:
            return Response({
                "status": False,
                "message": "Lesson not found in course",
                "can_access": False
            }, status=status.HTTP_404_NOT_FOUND)
        
        # Check previous lessons for incomplete tasks
        blocked_lessons = []
        for i in range(current_lesson_index):
            prev_lesson = course_lessons[i]
            # Get tasks for this lesson
            tasks = models.Task.objects.filter(lesson=prev_lesson)
            
            for task in tasks:
                # Check if user has submitted and been approved for this task
                submission = models.TaskAnswer.objects.filter(
                    task=task,
                    user=user
                ).first()
                
                if not submission or not submission.status or submission.status.title != 'تأیید شده':
                    blocked_lessons.append({
                        'lesson_id': prev_lesson.id,
                        'lesson_title': prev_lesson.title,
                        'task_id': task.id,
                        'task_title': task.title,
                        'submission_status': submission.status.title if submission and submission.status else 'Not submitted'
                    })
        
        can_access = len(blocked_lessons) == 0
        
        return Response({
            "status": True,
            "can_access": can_access,
            "blocked_lessons": blocked_lessons,
            "message": "Access granted" if can_access else "Complete previous tasks to access this lesson"
        }, status=status.HTTP_200_OK)


class TeacherTaskSubmissionsView(APIView):
    """Get tasks and submissions for teacher's courses"""
    authentication_classes = (CustomJWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        user = request.user
        
        # Get courses where user is mentor
        courses = models.Course.objects.filter(mentor=user)
        
        # Get all tasks created by this teacher
        teacher_tasks = models.Task.objects.filter(mentor=user).order_by('-create_date')
        
        # Prepare tasks data
        tasks_data = []
        for task in teacher_tasks:
            # Get submission count for this task
            submission_count = models.TaskAnswer.objects.filter(task=task).count()
            pending_count = models.TaskAnswer.objects.filter(task=task, status__title__in=['Pending Review', 'در انتظار بررسی']).count()
            
            tasks_data.append({
                'id': task.id,
                'title': task.title,
                'description': task.description,
                'difficulty': task.get_difficulty_display(),
                'file': request.build_absolute_uri(task.file.url) if task.file else None,
                'course': {
                    'id': task.course.id if task.course else None,
                    'title': task.course.title if task.course else 'بدون دوره',
                    'slug': task.course.slug if task.course else None
                },
                'lesson': {
                    'id': task.lesson.id,
                    'title': task.lesson.title
                } if task.lesson else None,
                'submission_count': submission_count,
                'pending_count': pending_count,
                'create_date': task.create_date,
                'update_date': task.update_date
            })
        
        # Get all submissions for teacher's tasks
        submissions_data = []
        for course in courses:
            # Get all tasks for this course
            tasks = models.Task.objects.filter(course=course)
            
            for task in tasks:
                # Get all submissions for this task
                submissions = models.TaskAnswer.objects.filter(task=task).select_related('user', 'status')
                
                for submission in submissions:
                    submissions_data.append({
                        'id': submission.id,
                        'task': {
                            'id': task.id,
                            'title': task.title,
                            'difficulty': task.get_difficulty_display(),
                            'lesson': {
                                'id': task.lesson.id,
                                'title': task.lesson.title
                            } if task.lesson else None
                        },
                        'course': {
                            'id': course.id,
                            'title': course.title,
                            'slug': course.slug
                        },
                        'student': {
                            'id': submission.user.id,
                            'first_name': submission.user.first_name,
                            'last_name': submission.user.last_name,
                            'phone_number': submission.user.phone_number
                        },
                        'submission': {
                            'id': submission.id,
                            'description': submission.description,
                            'file': request.build_absolute_uri(submission.file.url) if submission.file else None,
                            'status': submission.status.title if submission.status else 'در انتظار بررسی',
                            'submitted_at': submission.create_date,
                            'updated_at': submission.update_date
                        }
                    })
        
        # Sort submissions by submission date (newest first)
        submissions_data.sort(key=lambda x: x['submission']['submitted_at'], reverse=True)
        
        return Response({
            "status": True,
            "data": {
                "tasks": tasks_data,
                "submissions": submissions_data,
                "summary": {
                    "total_tasks": len(tasks_data),
                    "total_submissions": len(submissions_data),
                    "pending_submissions": len([s for s in submissions_data if s['submission']['status'] in ['Pending Review', 'در انتظار بررسی']])
                }
            }
        }, status=status.HTTP_200_OK)


class EditTaskView(APIView):
    authentication_classes = (CustomJWTAuthentication,)
    permission_classes = (IsAuthenticated,)
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        user = request.user

        # دریافت task_id از بدنه درخواست
        task_id = request.data.get("task_id")
        if not task_id:
            return Response({
                "status": False,
                "data": "شناسه تسک ارسال نشده است."
            }, status=status.HTTP_400_BAD_REQUEST)

        # پیدا کردن تسک
        task = get_object_or_404(models.Task, id=task_id)

        # بررسی اینکه کاربر منتور تسک است
        if task.mentor != user:
            return Response({
                "status": False,
                "data": "شما مجاز به ویرایش این تسک نیستید."
            }, status=status.HTTP_403_FORBIDDEN)

        # ویرایش تسک
        serializer = TaskSerializer(task, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({
                "status": True,
                "data": serializer.data
            }, status=status.HTTP_200_OK)

        return Response({
            "status": False,
            "data": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


class OrganizerCreateView(APIView):
    parser_classes = [MultiPartParser]
    authentication_classes = (CustomJWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        # چک نقش کاربر
        if not request.user.has_permission("user_manage"):
            return Response({
                'status': False,
                'data': {'error': 'You do not have permission to create an organizer.'}
            }, status=status.HTTP_403_FORBIDDEN)

        # بررسی اینکه آیا کاربر قبلاً Organizer دارد
        if hasattr(request.user, 'organizer'):
            return Response({
                'status': False,
                'data': {'error': 'You have already created an organizer.'}
            }, status=400)

        # ایجاد Organizer
        serializer = CreateOrganizerSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response({
                'status': True,
                'data': serializer.data
            }, status=201)
        return Response({
            'status': False,
            'data': serializer.errors
        }, status=400)


class OrganizerUpdateView(APIView):
    parser_classes = [MultiPartParser]
    authentication_classes = (CustomJWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        # پیدا کردن Organizer مرتبط با کاربر
        try:
            organizer = request.user.organizer
        except models.Organizer.DoesNotExist:
            return Response({
                'status': False,
                'data': {'error': 'Organizer not found.'}
            }, status=404)
        
        # چک مجوز: کاربر باید یا مجوز user_manage داشته باشد (ادمین) یا صاحب این organizer باشد
        has_admin_permission = request.user.has_permission("user_manage")
        is_owner = organizer.user == request.user
        
        if not (has_admin_permission or is_owner):
            return Response({
                'status': False,
                'data': {'error': 'You do not have permission to update this organizer.'}
            }, status=status.HTTP_403_FORBIDDEN)

        # ویرایش Organizer
        serializer = CreateOrganizerSerializer(organizer, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({
                'status': True,
                'data': serializer.data
            }, status=200)
        return Response({
            'status': False,
            'data': serializer.errors
        }, status=400)


# ------------------------------------------------------------------------------------------------------------------------
# create and update course, chapter and lesson by mohammad

class CourseCreateView(APIView):
    authentication_classes = (CustomJWTAuthentication,)
    permission_classes = (IsAuthenticated,)
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request):
        user = request.user

        # بررسی اینکه آیا نقش کاربر "مدرس" است یا نه
        if not user.has_permission("course_create"):
            return Response({
                "status": False,
                "message": "You do not have permission to create courses."
            }, status=status.HTTP_403_FORBIDDEN)

        # پیدا کردن Organizer مرتبط
        # اول بررسی می‌کنیم که آیا کاربر یک OrganizerTeacher است
        organizer_teacher = None
        organizer = None
        
        try:
            organizer_teacher = OrganizerTeacher.objects.get(user=user)
            organizer = organizer_teacher.organization
            
            # اگر کاربر OrganizerTeacher است، باید هم teacher و هم organizer تأیید شده باشند
            if not organizer_teacher.is_active or not organizer_teacher.is_verified:
                return Response({
                    "status": False,
                    "message": "Your organizer teacher profile is not active or not verified."
                }, status=status.HTTP_403_FORBIDDEN)
                
        except OrganizerTeacher.DoesNotExist:
            # اگر کاربر OrganizerTeacher نیست، بررسی می‌کنیم که آیا صاحب یک Organizer است
            try:
                organizer = user.organizer
            except Organizer.DoesNotExist:
                return Response({
                    "status": False,
                    "message": "You are not associated with any organizer."
                }, status=status.HTTP_400_BAD_REQUEST)

        # بررسی اینکه organizer فعال و تأیید شده است
        if not organizer.is_active or not organizer.is_verified:
            return Response({
                "status": False,
                "message": "Your organizer is not active or not verified. Please wait for admin verification."
            }, status=status.HTTP_403_FORBIDDEN)

        # حالا که نقش کاربر تأیید شد، داده‌ها به سریالایزر ارسال می‌شود
        data = request.data.copy()
        data['organizer'] = organizer.id  # اضافه کردن Organizer به داده‌های ورودی
        
        # اگر old_standard_code ارسال شده و suggestion_id هم ارسال شده، category و title را از suggestion بگیر
        old_standard_code = data.get('old_standard_code')
        suggestion_id = data.get('suggestion_id')
        
        if old_standard_code and suggestion_id:
            try:
                # پیدا کردن استاندارد بر اساس suggestion_id
                standard = models.Standards.objects.get(id=suggestion_id)
                
                # اگر category پیشنهادی وجود دارد، آن را ست کن
                if not data.get('category'):
                    # سعی کن category را بر اساس group_name یا cluster پیدا کنی
                    category = None
                    if standard.group_name:
                        category = models.Category.objects.filter(
                            title__icontains=standard.group_name
                        ).first()
                    
                    if not category and standard.cluster:
                        category = models.Category.objects.filter(
                            title__icontains=standard.cluster
                        ).first()
                    
                    if category:
                        data['category'] = category.id
                
                # اگر title ارسال نشده، از standard_name استفاده کن
                if not data.get('title') and standard.standard_name:
                    data['title'] = standard.standard_name
                
                # standard را هم ست کن
                if not data.get('standard'):
                    data['standard'] = standard.id
                    
            except models.Standards.DoesNotExist:
                pass  # اگر suggestion پیدا نشد، ادامه بده با داده‌های ارسالی

        serializer = CourseCreateSerializer(data=data, context={'request': request})

        if serializer.is_valid():
            course = serializer.save()
            # اطمینان از اینکه دوره جدید با is_published=False و is_verified=False ایجاد شود
            course.is_published = False
            course.is_verified = False
            course.save(update_fields=['is_published', 'is_verified'])

            # بررسی داده‌های attributes که به صورت JSON آمده‌اند
            attributes_data = request.data.get('attributes')
            if attributes_data:
                try:
                    # تبدیل داده‌های JSON به دیکشنری
                    attributes_data = json.loads(attributes_data)
                    for attr_data in attributes_data:
                        # ایجاد ویژگی‌ها
                        if 'attribute' in attr_data:
                            models.CourseAttribute.objects.create(
                                course=course,
                                attribute_id=attr_data['attribute'],
                                value=attr_data.get('value')
                            )
                        else:
                            return Response({
                                'status': False,
                                'message': 'Missing attribute data.'
                            }, status=status.HTTP_400_BAD_REQUEST)
                except json.JSONDecodeError:
                    return Response({
                        'status': False,
                        'message': 'Invalid attribute data format.'
                    }, status=status.HTTP_400_BAD_REQUEST)

            return Response({
                'status': True,
                'data': serializer.data
            }, status=status.HTTP_201_CREATED)

        return Response({
            'status': False,
            'data': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


class ChapterCreateView(APIView):
    authentication_classes = (CustomJWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        user = request.user
        course_id = request.data.get('course')

        try:
            course = models.Course.objects.get(id=course_id)
        except models.Course.DoesNotExist:
            return Response({
                "status": False,
                "message": "Course not found."
            }, status=status.HTTP_404_NOT_FOUND)

        # بررسی اینکه آیا کاربر مجاز به مدیریت این دوره است
        can_manage = False
        
        # بررسی 1: آیا کاربر صاحب دوره است؟
        if course.user == user:
            can_manage = True
        else:
            # بررسی 2: آیا کاربر صاحب organizer است؟
            try:
                if user.organizer == course.organizer:
                    if user.organizer.is_active and user.organizer.is_verified:
                        can_manage = True
            except Organizer.DoesNotExist:
                pass
            
            # بررسی 3: آیا کاربر یک OrganizerTeacher برای organizer این دوره است؟
            if not can_manage:
                try:
                    organizer_teacher = OrganizerTeacher.objects.get(
                        user=user,
                        organization=course.organizer
                    )
                    if (organizer_teacher.is_active and 
                        organizer_teacher.is_verified and 
                        course.organizer.is_active and 
                        course.organizer.is_verified):
                        can_manage = True
                except OrganizerTeacher.DoesNotExist:
                    pass

        if not can_manage:
            return Response({
                "status": False,
                "message": "You do not have permission to add a chapter to this course."
            }, status=status.HTTP_403_FORBIDDEN)

        serializer = ChapterCreateSerializer(data=request.data, context={'request': request})

        if serializer.is_valid():
            # چپتر ایجاد می‌شود
            serializer.save()
            return Response({
                'status': True,
                'data': serializer.data
            }, status=status.HTTP_201_CREATED)

        return Response({
            'status': False,
            'data': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


class LessonCreateView(APIView):
    authentication_classes = (CustomJWTAuthentication,)
    permission_classes = (IsAuthenticated,)
    parser_classes = (MultiPartParser, FormParser)  # برای ارسال فایل‌ها

    def post(self, request):
        user = request.user
        chapter_id = request.data.get('chapter')

        # بررسی وجود چپتر
        try:
            chapter = models.Chapter.objects.get(id=chapter_id)
        except models.Chapter.DoesNotExist:
            return Response({
                "status": False,
                "message": "Chapter not found."
            }, status=status.HTTP_404_NOT_FOUND)

        # بررسی اینکه آیا کاربر مجاز به مدیریت این دوره است
        course = chapter.course
        can_manage = False
        
        # بررسی 1: آیا کاربر صاحب دوره است؟
        if course.user == user:
            can_manage = True
        else:
            # بررسی 2: آیا کاربر صاحب organizer است؟
            try:
                if user.organizer == course.organizer:
                    if user.organizer.is_active and user.organizer.is_verified:
                        can_manage = True
            except Organizer.DoesNotExist:
                pass
            
            # بررسی 3: آیا کاربر یک OrganizerTeacher برای organizer این دوره است؟
            if not can_manage:
                try:
                    organizer_teacher = OrganizerTeacher.objects.get(
                        user=user,
                        organization=course.organizer
                    )
                    if (organizer_teacher.is_active and 
                        organizer_teacher.is_verified and 
                        course.organizer.is_active and 
                        course.organizer.is_verified):
                        can_manage = True
                except OrganizerTeacher.DoesNotExist:
                    pass

        if not can_manage:
            return Response({
                "status": False,
                "message": "You do not have permission to add a lesson to this chapter."
            }, status=status.HTTP_403_FORBIDDEN)

        # سریالایزر برای درس
        serializer = LessonCreateSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            lesson = serializer.save()
            # Ensure newly created lessons are not published until verified
            if lesson.is_published or lesson.is_verified:
                lesson.is_published = False
                lesson.is_verified = False
                lesson.save(update_fields=['is_published', 'is_verified'])

            return Response({
                'status': True,
                'data': serializer.data  # فایل‌ها نیز به صورت خودکار به این داده‌ها اضافه می‌شوند
            }, status=status.HTTP_201_CREATED)

        return Response({
            'status': False,
            'data': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


class UpdateCourseAPI(APIView):
    authentication_classes = (CustomJWTAuthentication,)
    permission_classes = (IsAuthenticated,)
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request):
        user = request.user
        course_id = request.data.get('course_id')

        if not course_id:
            return Response({
                'status': False,
                'data': 'course_id is required.'
            }, status=status.HTTP_400_BAD_REQUEST)

        # بررسی پرمیژن
        if not user.has_permission("course_edit"):
            return Response({
                'status': False,
                'data': 'You do not have permission to edit this course.'
            }, status=status.HTTP_403_FORBIDDEN)

        # بررسی مالکیت دوره
        try:
            course = models.Course.objects.get(id=course_id)
        except models.Course.DoesNotExist:
            return Response({
                'status': False,
                'data': 'Course not found.'
            }, status=status.HTTP_404_NOT_FOUND)

        # بررسی اینکه آیا کاربر مجاز به ویرایش این دوره است
        # کاربر می‌تواند دوره را ویرایش کند اگر:
        # 1. صاحب دوره باشد (course.user == user)
        # 2. صاحب organizer باشد (user.organizer == course.organizer)
        # 3. یک OrganizerTeacher برای organizer این دوره باشد
        
        can_edit = False
        
        # بررسی 1: آیا کاربر صاحب دوره است؟
        if course.user == user:
            can_edit = True
        else:
            # بررسی 2: آیا کاربر صاحب organizer است؟
            try:
                if user.organizer == course.organizer:
                    # بررسی اینکه organizer تأیید شده است
                    if user.organizer.is_active and user.organizer.is_verified:
                        can_edit = True
            except Organizer.DoesNotExist:
                pass
            
            # بررسی 3: آیا کاربر یک OrganizerTeacher برای organizer این دوره است؟
            if not can_edit:
                try:
                    organizer_teacher = OrganizerTeacher.objects.get(
                        user=user,
                        organization=course.organizer
                    )
                    if (organizer_teacher.is_active and 
                        organizer_teacher.is_verified and 
                        course.organizer.is_active and 
                        course.organizer.is_verified):
                        can_edit = True
                except OrganizerTeacher.DoesNotExist:
                    pass

        if not can_edit:
            return Response({
                'status': False,
                'data': 'You do not have permission to edit this course.'
            }, status=status.HTTP_403_FORBIDDEN)

        # سریالایزر برای ویرایش دوره
        serializer = CourseCreateSerializer(course, data=request.data, context={'request': request}, partial=True)
        if serializer.is_valid():
            serializer.save()

            # بررسی و به‌روزرسانی ویژگی‌های مرتبط
            attributes_data = request.data.get('attributes')
            if attributes_data:
                try:
                    # تبدیل داده‌های JSON به دیکشنری (همانند course creation)
                    attributes_data = json.loads(attributes_data)
                    for attr_data in attributes_data:
                        # به‌روزرسانی ویژگی‌ها
                        if 'attribute' in attr_data:
                            models.CourseAttribute.objects.update_or_create(
                                course=course,
                                attribute_id=attr_data['attribute'],
                                defaults={'value': attr_data.get('value')}
                            )
                        else:
                            return Response({
                                'status': False,
                                'data': 'Missing attribute data.'
                            }, status=status.HTTP_400_BAD_REQUEST)
                except json.JSONDecodeError:
                    return Response({
                        'status': False,
                        'data': 'Invalid attribute data format.'
                    }, status=status.HTTP_400_BAD_REQUEST)

            return Response({
                'status': True,
                'data': serializer.data
            }, status=status.HTTP_200_OK)

        return Response({
            'status': False,
            'data': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


class ChapterUpdateView(APIView):
    authentication_classes = (CustomJWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        user = request.user

        # آیدی چپتر را از بدنه درخواست می‌گیریم
        chapter_id = request.data.get('id')

        try:
            chapter = models.Chapter.objects.get(id=chapter_id)
        except models.Chapter.DoesNotExist:
            return Response({
                "status": False,
                "message": "Chapter not found."
            }, status=status.HTTP_404_NOT_FOUND)

        # کورس چپتر را می‌گیریم و بررسی می‌کنیم که آیا کاربر اجازه ویرایش آن را دارد
        course = chapter.course

        # بررسی اینکه آیا کاربر مجاز به مدیریت این دوره است
        can_manage = False
        
        # بررسی 1: آیا کاربر صاحب دوره است؟
        if course.user == user:
            can_manage = True
        else:
            # بررسی 2: آیا کاربر صاحب organizer است؟
            try:
                if user.organizer == course.organizer:
                    if user.organizer.is_active and user.organizer.is_verified:
                        can_manage = True
            except Organizer.DoesNotExist:
                pass
            
            # بررسی 3: آیا کاربر یک OrganizerTeacher برای organizer این دوره است؟
            if not can_manage:
                try:
                    organizer_teacher = OrganizerTeacher.objects.get(
                        user=user,
                        organization=course.organizer
                    )
                    if (organizer_teacher.is_active and 
                        organizer_teacher.is_verified and 
                        course.organizer.is_active and 
                        course.organizer.is_verified):
                        can_manage = True
                except OrganizerTeacher.DoesNotExist:
                    pass

        if not can_manage:
            return Response({
                "status": False,
                "message": "You do not have permission to update this chapter."
            }, status=status.HTTP_403_FORBIDDEN)

        # اضافه کردن کورس به داده‌ها قبل از ارسال به سریالایزر
        request.data['course'] = course.id

        # سریالایزر برای آپدیت چپتر
        serializer = ChapterCreateSerializer(chapter, data=request.data, context={'request': request})

        if serializer.is_valid():
            # چپتر آپدیت می‌شود
            serializer.save()
            return Response({
                'status': True,
                'data': serializer.data
            }, status=status.HTTP_200_OK)

        return Response({
            'status': False,
            'data': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


class UpdateLessonAPI(APIView):
    authentication_classes = (CustomJWTAuthentication,)
    permission_classes = (IsAuthenticated,)
    parser_classes = (MultiPartParser, FormParser)  # پشتیبانی از فرم دیتا و فایل‌ها

    def post(self, request):
        lesson_id = request.data.get('lesson_id')
        if not lesson_id:
            return Response({
                'status': False,
                'data': 'lesson_id is required.'
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            # بررسی وجود درس و مالکیت درس
            lesson = models.Lesson.objects.get(id=lesson_id)
            course = lesson.course
            user = request.user
            
            # بررسی اینکه آیا کاربر مجاز به مدیریت این دوره است
            can_manage = False
            
            # بررسی 1: آیا کاربر صاحب دوره است؟
            if course.user == user:
                can_manage = True
            else:
                # بررسی 2: آیا کاربر صاحب organizer است؟
                try:
                    if user.organizer == course.organizer:
                        if user.organizer.is_active and user.organizer.is_verified:
                            can_manage = True
                except Organizer.DoesNotExist:
                    pass
                
                # بررسی 3: آیا کاربر یک OrganizerTeacher برای organizer این دوره است؟
                if not can_manage:
                    try:
                        organizer_teacher = OrganizerTeacher.objects.get(
                            user=user,
                            organization=course.organizer
                        )
                        if (organizer_teacher.is_active and 
                            organizer_teacher.is_verified and 
                            course.organizer.is_active and 
                            course.organizer.is_verified):
                            can_manage = True
                    except OrganizerTeacher.DoesNotExist:
                        pass
            
            if not can_manage:
                return Response({
                    'status': False,
                    'data': 'You do not have permission to edit this lesson.'
                }, status=status.HTTP_403_FORBIDDEN)
        except models.Lesson.DoesNotExist:
            return Response({
                'status': False,
                'data': 'Lesson not found.'
            }, status=status.HTTP_404_NOT_FOUND)

        # سریالایزر برای به‌روزرسانی درس
        serializer = LessonUpdateSerializer(lesson, data=request.data, context={'request': request}, partial=True)
        if serializer.is_valid():
            # Saving lesson updates will trigger model logic to unverify/unpublish on content/title changes
            serializer.save()

            return Response({
                'status': True,
                'data': serializer.data
            }, status=status.HTTP_200_OK)

        return Response({
            'status': False,
            'data': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


# ------------------------------------------------------------------------------------------------------------------------
# this is for user course(teacher and student) list

class CourseUserPagination(PageNumberPagination):
    page_size = 10  # تعداد رکوردها در هر صفحه
    page_size_query_param = 'page_size'  # برای تنظیم اندازه صفحه از پارامتر URL
    max_page_size = 100  # حداکثر اندازه صفحه


class TeacherCoursesPagination(PageNumberPagination):
    page_size = 10  # تعداد رکوردها در هر صفحه
    page_size_query_param = 'page_size'  # امکان تغییر تعداد رکوردها از طریق پارامتر URL
    max_page_size = 100


class UserCoursesListView(APIView):
    authentication_classes = (CustomJWTAuthentication,)
    permission_classes = (IsAuthenticated,)  # فقط کاربران احراز هویت شده می‌توانند دسترسی داشته باشند
    parser_classes = (JSONParser, MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        user = request.user  # کاربر احراز هویت شده با JWT
        
        # Get view type from request data (default to 'enrolled' for students)
        view_type = request.data.get('view_type', 'enrolled')

        # Check user role and show appropriate courses
        if user.role and str(user.role) == 'دانشجو':
            # برای دانشجو: نمایش دوره‌های خریداری شده (فقط از سفارشات پرداخت شده)
            from payment.models import Order
            paid_course_ids = Order.objects.filter(
                user=user, 
                status__slug='completed'
            ).values_list('course_orders__course_id', flat=True)
            user_enrolled_courses = models.CourseUser.objects.filter(
                user=user, 
                course_id__in=paid_course_ids
            )
            
            if user_enrolled_courses.exists():
                # اعمال pagination
                paginator = CourseUserPagination()
                result_page = paginator.paginate_queryset(user_enrolled_courses, request)

                # سریالایز کردن داده‌ها
                serializer = CourseUserSerializer(result_page, many=True, context={'request': request})

                # ساختار پاسخ
                response_data = {
                    "status": True,
                    "role": "student",
                    "view_type": "enrolled",
                    "data": {
                        "count": paginator.page.paginator.count,
                        "next": paginator.get_next_link(),
                        "previous": paginator.get_previous_link(),
                        "results": serializer.data
                    }
                }
            else:
                # اگر دانشجو هیچ دوره‌ای خریداری نکرده
                response_data = {
                    "status": True,
                    "role": "student",
                    "view_type": "enrolled",
                    "data": {
                        "count": 0,
                        "next": None,
                        "previous": None,
                        "results": []
                    }
                }
                
        else:
            # برای غیر دانشجو (مدرس/مدیر): نمایش دوره‌های organization
            if hasattr(user, 'organizer') and user.organizer:
                # دوره‌های مربوط به organization کاربر
                organization_courses = models.Course.objects.filter(organizer=user.organizer)
            else:
                # اگر organization نداشت، دوره‌های ایجاد شده توسط کاربر
                organization_courses = models.Course.objects.filter(user=user)
            
            if organization_courses.exists():
                # اعمال صفحه‌بندی
                paginator = TeacherCoursesPagination()
                paginated_courses = paginator.paginate_queryset(organization_courses, request)

                # سریالایز کردن داده‌ها
                serializer = CourseListSerializer(paginated_courses, many=True, context={'request': request})

                # ساختار پاسخ
                response_data = {
                    "status": True,
                    "role": "teacher",
                    "view_type": "organization",
                    "data": {
                        "count": paginator.page.paginator.count,
                        "next": paginator.get_next_link(),
                        "previous": paginator.get_previous_link(),
                        "results": serializer.data
                    }
                }
            else:
                # اگر هیچ دوره‌ای نداشت
                response_data = {
                    "status": True,
                    "role": "teacher",
                    "view_type": "organization",
                    "data": {
                        "count": 0,
                        "next": None,
                        "previous": None,
                        "results": []
                    }
                }
        
        return Response(response_data, status=status.HTTP_200_OK)


class UserEnrolledCoursesListView(APIView):
    authentication_classes = (CustomJWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        user = request.user

        # Get user's enrolled courses
        user_enrolled_courses = models.CourseUser.objects.filter(user=user)
        
        if not user_enrolled_courses.exists():
            return Response({
                "status": True,
                "data": {
                    "count": 0,
                    "next": None,
                    "previous": None,
                    "results": []
                }
            }, status=status.HTTP_200_OK)

        # Paginate enrolled courses
        paginator = CourseUserPagination()
        result_page = paginator.paginate_queryset(user_enrolled_courses, request)
        serializer = CourseUserSerializer(result_page, many=True, context={'request': request})
        
        response_data = {
            "status": True,
            "data": {
                "count": paginator.page.paginator.count,
                "next": paginator.get_next_link(),
                "previous": paginator.get_previous_link(),
                "results": serializer.data
            }
        }
        
        return Response(response_data, status=status.HTTP_200_OK)


# ------------------------------------------------------------------------------------------------------------------------
# this is for teacher course detail

class TeacherCourseDetailView(APIView):
    authentication_classes = (CustomJWTAuthentication,)
    permission_classes = (IsAuthenticated,)  # فقط کاربران احراز هویت شده می‌توانند دسترسی داشته باشند

    def post(self, request, *args, **kwargs):
        teacher = request.user  # مدرس از طریق JWT تشخیص داده می‌شود

        # گرفتن course_id از بادی درخواست
        course_id = request.data.get('course_id')
        if not course_id:
            return Response({
                "status": False,
                "data": {"error": "Course ID is required."}
            }, status=status.HTTP_400_BAD_REQUEST)

        # پیدا کردن دوره مربوط به مدرس یا organizer
        try:
            course = models.Course.objects.get(id=course_id)
            
            # بررسی اینکه آیا کاربر صاحب دوره است یا صاحب organizer است
            can_access = False
            
            # بررسی 1: آیا کاربر صاحب دوره است؟
            if course.user == teacher:
                can_access = True
            else:
                # بررسی 2: آیا کاربر صاحب organizer است؟
                try:
                    if teacher.organizer == course.organizer:
                        if teacher.organizer.is_active and teacher.organizer.is_verified:
                            can_access = True
                except Organizer.DoesNotExist:
                    pass
                
                # بررسی 3: آیا کاربر یک OrganizerTeacher برای organizer این دوره است؟
                if not can_access:
                    try:
                        organizer_teacher = OrganizerTeacher.objects.get(
                            user=teacher,
                            organization=course.organizer
                        )
                        if (organizer_teacher.is_active and 
                            organizer_teacher.is_verified and 
                            course.organizer.is_active and 
                            course.organizer.is_verified):
                            can_access = True
                    except OrganizerTeacher.DoesNotExist:
                        pass
            
            if not can_access:
                return Response({
                    "status": False,
                    "data": {"error": "Course not found or you do not have permission to access this course."}
                }, status=status.HTTP_403_FORBIDDEN)
                
        except models.Course.DoesNotExist:
            return Response({
                "status": False,
                "data": {"error": "Course not found."}
            }, status=status.HTTP_404_NOT_FOUND)

        # سریالایز کردن داده‌های دوره با استفاده از TeacherCourseSerializer
        serializer = TeacherCourseSerializer(course, context={'request': request})

        # ساختار پاسخ استاندارد
        response_data = {
            "status": True,
            "data": serializer.data
        }

        return Response(response_data, status=status.HTTP_200_OK)


# ----------------------------------------------------------------------------------------------------------------------
# this is for task list for user (student or mentor)

class UserTasksListView(APIView):
    authentication_classes = (CustomJWTAuthentication,)
    permission_classes = (IsAuthenticated,)  # کاربر باید لاگین کرده باشد

    def post(self, request, *args, **kwargs):
        user = request.user

        # بررسی نقش کاربر
        if user.has_permission("task_view"):
            # دریافت لیست تسک‌های منتور
            tasks = models.Task.objects.filter(mentor=user)

        else:
            return Response({
                "status": False,
                "data": "You do not have permission to view tasks."
            }, status=status.HTTP_403_FORBIDDEN)

        # سریالایز و بازگرداندن داده‌ها
        serializer = TaskSerializer(tasks, many=True, context={'request': request})
        return Response({
            "status": True,
            "data": serializer.data
        }, status=status.HTTP_200_OK)


# -----------------------------------------------------------------------------------------------------------------------
# this is for OrganizationsList


class OrganizationListPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class OrganizerListView(APIView):
    def post(self, request, *args, **kwargs):
        # دریافت پارامترهای pagination از request body
        page = request.data.get('page', 1)
        page_size = request.data.get('page_size', 10)
        
        # فیلتر کردن آموزشگاه‌های فعال و تایید شده
        organizers = Organizer.objects.filter(is_active=True, is_verified=True)
        
        # مرتب‌سازی بر اساس display_order (صعودی) و سپس create_date (نزولی)
        # اگر display_order null باشد، به عنوان 9999 در نظر گرفته می‌شود
        from django.db.models import F, Case, When, IntegerField
        organizers = organizers.annotate(
            order_value=Case(
                When(display_order__isnull=True, then=9999),
                default=F('display_order'),
                output_field=IntegerField()
            )
        ).order_by('order_value', '-create_date')
        
        # Manual pagination برای loadmore
        total_count = organizers.count()
        start_index = (page - 1) * page_size
        end_index = start_index + page_size
        paginated_organizers = organizers[start_index:end_index]
        
        serializer = OrganizationListSerializer(paginated_organizers, many=True, context={'request': request})
        
        # محاسبه next page
        has_next = end_index < total_count
        next_page = page + 1 if has_next else None
        
        response_data = {
            "status": True,
            "data": {
                "count": total_count,
                "page": page,
                "page_size": page_size,
                "has_next": has_next,
                "next_page": next_page,
                "data": serializer.data
            }
        }
        
        return Response(response_data, status=status.HTTP_200_OK)


class OrganizerBySlugView(APIView):
    """
    دریافت اطلاعات یک آموزشگاه با slug.
    فرمت پاسخ مثل course/organization/list است (یک آیتم).
    """
    def post(self, request, *args, **kwargs):
        slug = request.data.get('slug')
        if not slug or not str(slug).strip():
            return Response({
                "status": False,
                "data": {"error": "slug is required"}
            }, status=status.HTTP_400_BAD_REQUEST)

        slug = str(slug).strip()
        organizer = Organizer.objects.filter(
            slug=slug,
            is_active=True,
            is_verified=True
        ).first()

        if not organizer:
            return Response({
                "status": False,
                "data": {"error": "Organizer not found."}
            }, status=status.HTTP_404_NOT_FOUND)

        serializer = OrganizationListSerializer(organizer, context={'request': request})
        response_data = {
            "status": True,
            "data": {
                "count": 1,
                "page": 1,
                "page_size": 1,
                "has_next": False,
                "next_page": None,
                "data": [serializer.data]
            }
        }
        return Response(response_data, status=status.HTTP_200_OK)


class UserOrganizerDetailView(APIView):
    authentication_classes = (CustomJWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        try:
            # Get current user's organizer
            organizer = request.user.organizer
            serializer = CreateOrganizerSerializer(organizer, context={'request': request})
            
            return Response({
                'status': True,
                'data': serializer.data
            }, status=status.HTTP_200_OK)
            
        except Organizer.DoesNotExist:
            return Response({
                'status': False,
                'data': {'error': 'No organizer found for this user.'}
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({
                'status': False,
                'data': {'error': str(e)}
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class SubdomainOrganizerView(APIView):
    """
    نمایش صفحه organizer بر اساس subdomain
    این view زمانی فراخوانی می‌شود که کاربر با subdomain وارد شده باشد
    """
    
    def get(self, request, *args, **kwargs):
        # دریافت organizer از middleware
        organizer = getattr(request, 'organizer', None)
        
        if not organizer:
            return Response({
                'status': False,
                'data': {'error': 'Organizer not found.'}
            }, status=status.HTTP_404_NOT_FOUND)
        
        # سریالایز کردن اطلاعات organizer
        from .serializers import CreateOrganizerSerializer
        serializer = CreateOrganizerSerializer(organizer, context={'request': request})
        
        # دریافت دوره‌های این organizer
        courses = models.Course.objects.filter(
            organizer=organizer,
            is_active=True
        ).order_by('-create_date')[:10]  # 10 دوره اخیر
        
        from .serializers import PublicCourseSerializer
        courses_serializer = PublicCourseSerializer(courses, many=True, context={'request': request})
        
        return Response({
            'status': True,
            'data': {
                'organizer': serializer.data,
                'courses': courses_serializer.data
            }
        }, status=status.HTTP_200_OK)
    
    def post(self, request, *args, **kwargs):
        # برای POST هم همان منطق GET را اجرا می‌کنیم
        return self.get(request, *args, **kwargs)


class CheckDomainView(APIView):
    """
    بررسی اینکه آیا subdomain در دسترس است یا نه
    اگر organizer وجود داشت، اطلاعات کامل آن را برمی‌گرداند
    پشتیبانی از GET و POST
    """
    
    def _get_subdomain(self, request):
        """استخراج subdomain از request (GET یا POST)"""
        # اول از query parameters (GET) بررسی می‌کنیم
        subdomain = request.GET.get('subdomain', None)
        
        # اگر در GET نبود، از request data (POST) بررسی می‌کنیم
        if not subdomain:
            if hasattr(request, 'data'):
                subdomain = request.data.get('subdomain', None)
        
        return subdomain
    
    def _check_domain(self, request, subdomain):
        """منطق اصلی بررسی subdomain"""
        if not subdomain:
            return Response({
                'status': False,
                'message': 'subdomain parameter is required',
                'data': None
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # پاک کردن subdomain (حذف فضاهای خالی و تبدیل به lowercase)
        subdomain = subdomain.strip().lower()
        
        # حذف .onsho24.ir اگر وجود داشته باشد
        subdomain = subdomain.replace('.onsho24.ir', '').replace('onsho24.ir', '')
        
        # بررسی subdomain های غیرمجاز
        reserved_subdomains = ['www', 'api', 'admin', 'mail', 'ftp', 'cpanel']
        if subdomain in reserved_subdomains:
            return Response({
                'status': True,
                'data': {
                    'available': False,
                    'message': 'This subdomain is reserved and cannot be used'
                }
            }, status=status.HTTP_200_OK)
        
        # بررسی اینکه آیا این subdomain قبلاً استفاده شده است
        # فقط سازمان‌های فعال را بررسی می‌کنیم
        try:
            # استفاده از filter().first() برای اطمینان از یافتن organizer
            # جستجو با subdomain__iexact برای تطابق case-insensitive
            # فقط سازمان‌های فعال را بررسی می‌کنیم
            organizer = Organizer.objects.filter(
                subdomain__iexact=subdomain,
                is_active=True
            ).first()
            
            # اگر با iexact پیدا نشد، سعی می‌کنیم با strip و lowercase هم جستجو کنیم
            if not organizer:
                # جستجوی دقیق‌تر با strip کردن مقادیر دیتابیس
                # فقط سازمان‌های فعال
                all_organizers = Organizer.objects.filter(
                    is_active=True
                ).exclude(subdomain__isnull=True).exclude(subdomain='')
                for org in all_organizers:
                    if org.subdomain and org.subdomain.strip().lower() == subdomain.strip().lower():
                        organizer = org
                        break
            
            if organizer:
                # ساخت URL کامل برای logo
                logo_url = ''
                if organizer.logo:
                    logo_url = request.build_absolute_uri(organizer.logo.url)
                
                # برگرداندن اطلاعات کامل organizer (مطابق با فرمت مورد انتظار)
                return Response({
                    'status': True,
                    'data': {
                        'available': False,
                        'organizer_id': organizer.id,
                        'organizer_name': organizer.name,
                        'slug': organizer.slug or '',  # ⚠️ مهم: حتماً slug را می‌فرستیم
                        'id': organizer.id,
                        'name': organizer.name,
                        'logo': logo_url,
                        'description': organizer.description or '',
                        'website_url': organizer.website_url or '',
                        'domain': organizer.subdomain or '',  # domain همان subdomain است
                        'is_active': organizer.is_active,
                        'is_verified': organizer.is_verified,
                    }
                }, status=status.HTTP_200_OK)
            else:
                # Subdomain وجود ندارد (در دسترس است)
                return Response({
                    'status': True,
                    'data': {
                        'available': True,
                        'message': 'This subdomain is available'
                    }
                }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                'status': False,
                'message': f'خطا در بررسی دامنه: {str(e)}',
                'data': None
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def get(self, request, *args, **kwargs):
        """پشتیبانی از GET request"""
        subdomain = self._get_subdomain(request)
        return self._check_domain(request, subdomain)
    
    def post(self, request, *args, **kwargs):
        """پشتیبانی از POST request"""
        subdomain = self._get_subdomain(request)
        return self._check_domain(request, subdomain)


# ------------------------------------------------------------------------------------------------------------------------
# Modares (Mentor) List View
class ModaresListView(APIView):
    """
    لیست دوره‌های مدرس برای انتخاب در فرم ایجاد تمرین
    این endpoint لیست دوره‌های مرتبط با organizer کاربر را برمی‌گرداند
    """
    authentication_classes = (CustomJWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        user = request.user
        
        # دریافت دوره‌های مرتبط با organizer کاربر
        courses = None
        
        # اگر کاربر organizer دارد، دوره‌های مرتبط با organizer را برگردان
        try:
            organizer = user.organizer
            # دریافت همه دوره‌های مرتبط با این organizer
            courses = models.Course.objects.filter(organizer=organizer).select_related('category', 'organizer')
        except Organizer.DoesNotExist:
            # اگر کاربر organizer ندارد، دوره‌های ایجاد شده توسط کاربر را برگردان
            courses = models.Course.objects.filter(user=user).select_related('category', 'organizer')
        
        if courses is None:
            courses = models.Course.objects.none()
        
        # سریالایز کردن داده‌ها
        serializer = CourseListSerializer(courses, many=True, context={'request': request})
        
        # ساختار پاسخ مطابق با مستندات
        return Response({
            'status': True,
            'data': serializer.data
        }, status=status.HTTP_200_OK)


class MentorListAPIView(APIView):
    """
    لیست منتورها (استادها) برای انتخاب در فرم ایجاد/ویرایش دوره
    این endpoint لیست منتورهای مرتبط با organizer کاربر را برمی‌گرداند
    """
    authentication_classes = (CustomJWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        user = request.user
        
        # لیست منتورها
        mentors_data = []
        
        # اگر کاربر organizer دارد، منتورهای مرتبط با organizer را برگردان
        try:
            organizer = user.organizer
            # دریافت همه OrganizerTeacher های مرتبط با این organizer
            organizer_teachers = OrganizerTeacher.objects.filter(
                organization=organizer,
                is_active=True
            ).select_related('user')
            
            for teacher in organizer_teachers:
                mentors_data.append({
                    'id': teacher.user.id,
                    'first_name': teacher.user.first_name or '',
                    'last_name': teacher.user.last_name or '',
                    'phone_number': teacher.user.phone_number,
                    'full_name': f"{teacher.user.first_name or ''} {teacher.user.last_name or ''}".strip() or teacher.user.phone_number,
                    'is_verified': teacher.is_verified,
                    'is_active': teacher.is_active,
                })
        except Organizer.DoesNotExist:
            # اگر کاربر organizer ندارد، لیست خالی برگردان
            pass
        
        # اگر هیچ منتوری پیدا نشد، لیست خالی برگردان
        return Response({
            'status': True,
            'data': mentors_data
        }, status=status.HTTP_200_OK)


# ------------------------------------------------------------------------------------------------------------------------
# this is for create taskanswer

class TaskAnswerView(APIView):
    authentication_classes = (CustomJWTAuthentication,)
    permission_classes = (IsAuthenticated,)  # کاربر باید لاگین کرده باشد

    def post(self, request, *args, **kwargs):
        task_id = request.data.get("task_id")
        user = request.user
        description = request.data.get("description", "")
        file = request.FILES.get("file")
        deadline = request.data.get("deadline")

        if not task_id:
            return Response({"status": False, "message": "task_id is required", "data": None},
                            status=status.HTTP_400_BAD_REQUEST)

        task = get_object_or_404(models.Task, id=task_id)
        pending_status = get_object_or_404(models.AnswerStatus, title="Pending Review")

        formatted_deadline = None
        if deadline:
            date_formats = ["%Y-%m-%d %H:%M:%S", "%Y-%m-%dT%H:%M:%S", "%Y-%m-%d %H:%M"]  # پشتیبانی از چندین فرمت
            for date_format in date_formats:
                try:
                    formatted_deadline = datetime.strptime(deadline, date_format)
                    break  # اگر تبدیل موفق شد، حلقه را متوقف کن
                except ValueError:
                    continue

            if formatted_deadline is None:
                return Response({"status": False,
                                 "message": "فرمت تاریخ نامعتبر است. از قالب YYYY-MM-DD HH:MM:SS یا YYYY-MM-DD HH:MM استفاده کنید."},
                                status=status.HTTP_400_BAD_REQUEST)

        task_answer = models.TaskAnswer.objects.create(
            task=task,
            user=user,
            description=description,
            file=file,
            deadline=formatted_deadline,
            status=pending_status
        )

        serializer = TaskAnswerSerializer(task_answer, context={'request': request})
        return Response({"status": True, "data": serializer.data}, status=status.HTTP_201_CREATED)


# ------------------------------------------------------------------------------------------------------------------------
# this is for changing the status of a task by mentor

class UpdateTaskAnswerStatusAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        answer_id = request.data.get("answer_id")
        status_slug = request.data.get("status_slug")
        user = request.user

        if not answer_id or not status_slug:
            return Response({"status": False, "message": "answer_id and status_slug are required", "data": None},
                            status=status.HTTP_400_BAD_REQUEST)

        if not user.has_permission("task_grade"):
            return Response({"status": False, "message": "You do not have permission to change task status."},
                            status=status.HTTP_403_FORBIDDEN)

        task_answer = get_object_or_404(models.TaskAnswer, id=answer_id)

        if task_answer.task.mentor != user:
            return Response({"status": False,
                             "message": "You do not have permission to update this answer's status. Only the mentor of the related task can perform this action."},
                            status=status.HTTP_403_FORBIDDEN)

        # Map status slug to title
        status_title_map = {
            'approved': 'Approved',
            'rejected': 'Rejected',
            'pending': 'Pending Review',
            'under_review': 'Under Review',
            'needs_revision': 'Needs Revision'
        }
        
        status_title = status_title_map.get(status_slug, status_slug)
        new_status = get_object_or_404(models.AnswerStatus, title=status_title)
        task_answer.status = new_status
        task_answer.save()

        serializer = AnswerListSerializer(task_answer, context={'request': request})
        return Response({"status": True, "data": serializer.data}, status=status.HTTP_200_OK)


# ------------------------------------------------------------------------------------------------------------------------
# this if for taskdetail

class TaskDetailAPIView(APIView):
    def post(self, request, *args, **kwargs):
        task_id = request.data.get("task_id")
        if not task_id:
            return Response({"status": False, "message": "task_id is required", "data": None},
                            status=status.HTTP_400_BAD_REQUEST)

        task = get_object_or_404(models.Task, id=task_id)
        serializer = TaskDetailSerializer(task, context={'request': request})

        return Response({"status": True, "data": serializer.data}, status=status.HTTP_200_OK)


# ------------------------------------------------------------------------------------------------------------------------
# Organization Teacher Management Views

class OrganizationTeachersListView(APIView):
    authentication_classes = (CustomJWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        try:
            # Get current user's organization
            organizer_teacher = OrganizerTeacher.objects.get(user=request.user)
            organization = organizer_teacher.organization
            
            # Get all teachers in this organization
            teachers = OrganizerTeacher.objects.filter(organization=organization).select_related('user')
            
            # Serialize the data
            teachers_data = []
            for teacher in teachers:
                teachers_data.append({
                    'id': teacher.id,
                    'user_id': teacher.user.id,
                    'first_name': teacher.user.first_name,
                    'last_name': teacher.user.last_name,
                    'phone_number': teacher.user.phone_number,
                    'is_active': teacher.is_active,
                    'is_verified': teacher.is_verified,
                    'create_date': teacher.create_date,
                    'update_date': teacher.update_date
                })
            
            return Response({
                'status': True,
                'data': teachers_data
            }, status=status.HTTP_200_OK)
            
        except OrganizerTeacher.DoesNotExist:
            return Response({
                'status': False,
                'message': 'You are not associated with any organization.'
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({
                'status': False,
                'message': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class OrganizationTeacherToggleView(APIView):
    authentication_classes = (CustomJWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        try:
            teacher_id = request.data.get('teacher_id')
            action = request.data.get('action')  # 'activate' or 'deactivate'
            
            if not teacher_id or not action:
                return Response({
                    'status': False,
                    'message': 'teacher_id and action are required'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Get current user's organization
            current_organizer_teacher = OrganizerTeacher.objects.get(user=request.user)
            organization = current_organizer_teacher.organization
            
            # Get the target teacher
            target_teacher = OrganizerTeacher.objects.get(
                id=teacher_id,
                organization=organization
            )
            
            # Update the teacher status
            if action == 'activate':
                target_teacher.is_active = True
            elif action == 'deactivate':
                target_teacher.is_active = False
            else:
                return Response({
                    'status': False,
                    'message': 'Invalid action. Use "activate" or "deactivate"'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            target_teacher.save()
            
            return Response({
                'status': True,
                'message': f'Teacher {action}d successfully',
                'data': {
                    'id': target_teacher.id,
                    'is_active': target_teacher.is_active,
                    'is_verified': target_teacher.is_verified
                }
            }, status=status.HTTP_200_OK)
            
        except OrganizerTeacher.DoesNotExist:
            return Response({
                'status': False,
                'message': 'Teacher not found or you do not have permission to manage this teacher.'
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({
                'status': False,
                'message': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class OrganizationTeacherVerifyView(APIView):
    authentication_classes = (CustomJWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        try:
            teacher_id = request.data.get('teacher_id')
            action = request.data.get('action')  # 'verify' or 'unverify'
            
            if not teacher_id or not action:
                return Response({
                    'status': False,
                    'message': 'teacher_id and action are required'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Get current user's organization
            current_organizer_teacher = OrganizerTeacher.objects.get(user=request.user)
            organization = current_organizer_teacher.organization
            
            # Get the target teacher
            target_teacher = OrganizerTeacher.objects.get(
                id=teacher_id,
                organization=organization
            )
            
            # Update the teacher verification status
            if action == 'verify':
                target_teacher.is_verified = True
            elif action == 'unverify':
                target_teacher.is_verified = False
            else:
                return Response({
                    'status': False,
                    'message': 'Invalid action. Use "verify" or "unverify"'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            target_teacher.save()
            
            return Response({
                'status': True,
                'message': f'Teacher {action}d successfully',
                'data': {
                    'id': target_teacher.id,
                    'is_active': target_teacher.is_active,
                    'is_verified': target_teacher.is_verified
                }
            }, status=status.HTTP_200_OK)
            
        except OrganizerTeacher.DoesNotExist:
            return Response({
                'status': False,
                'message': 'Teacher not found or you do not have permission to manage this teacher.'
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({
                'status': False,
                'message': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class OrganizationAddTeacherView(APIView):
    authentication_classes = (CustomJWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        try:
            phone_number = request.data.get('phone_number')
            
            if not phone_number:
                return Response({
                    'status': False,
                    'message': 'phone_number is required'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Get current user's organization
            current_organizer_teacher = OrganizerTeacher.objects.get(user=request.user)
            organization = current_organizer_teacher.organization
            
            # Find user by phone number
            try:
                user = User.objects.get(phone_number=phone_number)
            except User.DoesNotExist:
                return Response({
                    'status': False,
                    'message': 'User with this phone number not found'
                }, status=status.HTTP_404_NOT_FOUND)
            
            # Check if user is already a teacher in this organization
            if OrganizerTeacher.objects.filter(user=user, organization=organization).exists():
                return Response({
                    'status': False,
                    'message': 'This user is already a teacher in your organization'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Check if user is a teacher in another organization
            if OrganizerTeacher.objects.filter(user=user).exists():
                return Response({
                    'status': False,
                    'message': 'This user is already a teacher in another organization'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Create new teacher relationship
            new_teacher = OrganizerTeacher.objects.create(
                user=user,
                organization=organization,
                is_active=True,  # Default to active
                is_verified=False  # Default to unverified, needs manual verification
            )
            
            return Response({
                'status': True,
                'message': 'Teacher added successfully',
                'data': {
                    'id': new_teacher.id,
                    'user_id': user.id,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'phone_number': user.phone_number,
                    'is_active': new_teacher.is_active,
                    'is_verified': new_teacher.is_verified,
                    'create_date': new_teacher.create_date
                }
            }, status=status.HTTP_201_CREATED)
            
        except OrganizerTeacher.DoesNotExist:
            return Response({
                'status': False,
                'message': 'You are not associated with any organization.'
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({
                'status': False,
                'message': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# ------------------------------------------------------------------------------------------------------------------------
# this if for answerlist

class AnswerListAPIView(APIView):
    authentication_classes = (CustomJWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        answers = models.TaskAnswer.objects.select_related("user", "task").all()
        serializer = AnswerListSerializer(answers, many=True, context={'request': request})

        return Response({"status": True, "data": serializer.data}, status=status.HTTP_200_OK)


# ------------------------------------------------------------------------------------------------------------------------
# this if for answerdetail

class AnswerDetailAPIView(APIView):

    def post(self, request, *args, **kwargs):
        answer_id = request.data.get("answer_id")
        if not answer_id:
            return Response({"status": False, "message": "answer_id is required", "data": None},
                            status=status.HTTP_400_BAD_REQUEST)

        task_answer = get_object_or_404(models.TaskAnswer, id=answer_id)
        serializer = AnswerListSerializer(task_answer, context={'request': request})

        return Response({"status": True, "data": serializer.data}, status=status.HTTP_200_OK)


# ------------------------------------------------------------------------------------------------------------------------
# Standards Views

class StandardsPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100


class StandardsListView(APIView):
    """List all standards with filtering and pagination"""
    pagination_class = StandardsPagination
    
    def post(self, request, *args, **kwargs):
        search_query = request.data.get('search', None)
        cluster = request.data.get('cluster', None)
        group_name = request.data.get('group_name', None)
        standard_type = request.data.get('type', None)
        parent_id = request.data.get('parent_id', None)
        level = request.data.get('level', None)
        ordering = request.data.get('ordering', 'number')
        page = request.data.get('page', 1)
        page_size = request.data.get('page_size', 20)
        
        standards = models.Standards.objects.all()
        
        # Apply filters
        if search_query:
            standards = standards.filter(
                models.Q(standard_name__icontains=search_query) |
                models.Q(standard_name_latin__icontains=search_query) |
                models.Q(old_standard_code__icontains=search_query)
            )
        
        if cluster:
            standards = standards.filter(cluster=cluster)
        
        if group_name:
            standards = standards.filter(group_name=group_name)
        
        if standard_type:
            standards = standards.filter(type=standard_type)
        
        if parent_id:
            standards = standards.filter(parent_id=parent_id)
        elif parent_id is False:  # Only root standards
            standards = standards.filter(parent__isnull=True)
        
        if level is not None:
            # Filter by level (this requires a custom filter since level is a property)
            filtered_standards = []
            for standard in standards:
                if standard.level == level:
                    filtered_standards.append(standard.id)
            standards = standards.filter(id__in=filtered_standards)
        
        # Apply ordering
        standards = standards.order_by(ordering)
        
        # Apply pagination
        paginator = self.pagination_class()
        paginated_standards = paginator.paginate_queryset(standards, request)
        
        serializer = StandardsListSerializer(paginated_standards, many=True, context={'request': request})
        
        return Response({
            "status": True,
            "data": serializer.data,
            "pagination": {
                "count": paginator.page.paginator.count,
                "next": paginator.get_next_link(),
                "previous": paginator.get_previous_link(),
                "current_page": paginator.page.number,
                "total_pages": paginator.page.paginator.num_pages,
                "page_size": paginator.page_size
            }
        }, status=status.HTTP_200_OK)


class StandardsTreeView(APIView):
    """Get standards in tree structure"""
    
    def post(self, request, *args, **kwargs):
        root_only = request.data.get('root_only', True)
        cluster = request.data.get('cluster', None)
        group_name = request.data.get('group_name', None)
        
        if root_only:
            standards = models.Standards.objects.filter(parent__isnull=True)
        else:
            standards = models.Standards.objects.all()
        
        # Apply filters
        if cluster:
            standards = standards.filter(cluster=cluster)
        
        if group_name:
            standards = standards.filter(group_name=group_name)
        
        standards = standards.order_by('number')
        serializer = RecursiveStandardsSerializer(standards, many=True, context={'request': request})
        
        return Response({
            "status": True,
            "data": serializer.data
        }, status=status.HTTP_200_OK)


class StandardsDetailView(APIView):
    """Get detailed information about a specific standard"""
    
    def post(self, request, *args, **kwargs):
        standard_id = request.data.get('standard_id', None)
        slug = request.data.get('slug', None)
        
        if not standard_id and not slug:
            return Response({
                "status": False,
                "message": "standard_id or slug is required",
                "data": None
            }, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            if standard_id:
                standard = get_object_or_404(models.Standards, id=standard_id)
            else:
                standard = get_object_or_404(models.Standards, slug=slug)
            
            serializer = StandardsDetailSerializer(standard, context={'request': request})
            
            return Response({
                "status": True,
                "data": serializer.data
            }, status=status.HTTP_200_OK)
            
        except models.Standards.DoesNotExist:
            return Response({
                "status": False,
                "message": "Standard not found",
                "data": None
            }, status=status.HTTP_404_NOT_FOUND)


class StandardsCreateView(APIView):
    """Create a new standard - Only for admins and managers"""
    authentication_classes = [CustomJWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    def post(self, request, *args, **kwargs):
        # Check if user has permission to create standards
        user = request.user
        if not (user.has_permission('standards_manage') or user.is_superuser):
            return Response({
                "status": False,
                "message": "You don't have permission to create standards",
                "data": None
            }, status=status.HTTP_403_FORBIDDEN)
        
        serializer = StandardsCreateUpdateSerializer(data=request.data)
        
        if serializer.is_valid():
            standard = serializer.save()
            response_serializer = StandardsDetailSerializer(standard, context={'request': request})
            
            return Response({
                "status": True,
                "message": "Standard created successfully",
                "data": response_serializer.data
            }, status=status.HTTP_201_CREATED)
        
        return Response({
            "status": False,
            "message": "Validation error",
            "errors": serializer.errors,
            "data": None
        }, status=status.HTTP_400_BAD_REQUEST)


class StandardsUpdateView(APIView):
    """Update an existing standard - Only for admins and managers"""
    authentication_classes = [CustomJWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    def post(self, request, *args, **kwargs):
        # Check if user has permission to update standards
        user = request.user
        if not (user.has_permission('standards_manage') or user.is_superuser):
            return Response({
                "status": False,
                "message": "You don't have permission to update standards",
                "data": None
            }, status=status.HTTP_403_FORBIDDEN)
        
        standard_id = request.data.get('standard_id', None)
        
        if not standard_id:
            return Response({
                "status": False,
                "message": "standard_id is required",
                "data": None
            }, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            standard = get_object_or_404(models.Standards, id=standard_id)
            serializer = StandardsCreateUpdateSerializer(standard, data=request.data, partial=True)
            
            if serializer.is_valid():
                updated_standard = serializer.save()
                response_serializer = StandardsDetailSerializer(updated_standard, context={'request': request})
                
                return Response({
                    "status": True,
                    "message": "Standard updated successfully",
                    "data": response_serializer.data
                }, status=status.HTTP_200_OK)
            
            return Response({
                "status": False,
                "message": "Validation error",
                "errors": serializer.errors,
                "data": None
            }, status=status.HTTP_400_BAD_REQUEST)
            
        except models.Standards.DoesNotExist:
            return Response({
                "status": False,
                "message": "Standard not found",
                "data": None
            }, status=status.HTTP_404_NOT_FOUND)


class StandardsDeleteView(APIView):
    """Delete a standard - Only for admins and managers"""
    authentication_classes = [CustomJWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    def post(self, request, *args, **kwargs):
        # Check if user has permission to delete standards
        user = request.user
        if not (user.has_permission('standards_manage') or user.is_superuser):
            return Response({
                "status": False,
                "message": "You don't have permission to delete standards",
                "data": None
            }, status=status.HTTP_403_FORBIDDEN)
        
        standard_id = request.data.get('standard_id', None)
        
        if not standard_id:
            return Response({
                "status": False,
                "message": "standard_id is required",
                "data": None
            }, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            standard = get_object_or_404(models.Standards, id=standard_id)
            
            # Check if standard has children
            if standard.children.exists():
                return Response({
                    "status": False,
                    "message": "Cannot delete standard with children. Please delete children first.",
                    "data": None
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Check if standard is being used by any courses
            if standard.courses.exists():
                return Response({
                    "status": False,
                    "message": "Cannot delete standard that is being used by courses.",
                    "data": None
                }, status=status.HTTP_400_BAD_REQUEST)
            
            standard.delete()
            
            return Response({
                "status": True,
                "message": "Standard deleted successfully",
                "data": None
            }, status=status.HTTP_200_OK)
            
        except models.Standards.DoesNotExist:
            return Response({
                "status": False,
                "message": "Standard not found",
                "data": None
            }, status=status.HTTP_404_NOT_FOUND)


class StandardsChildrenView(APIView):
    """Get children of a specific standard"""
    
    def post(self, request, *args, **kwargs):
        standard_id = request.data.get('standard_id', None)
        slug = request.data.get('slug', None)
        
        if not standard_id and not slug:
            return Response({
                "status": False,
                "message": "standard_id or slug is required",
                "data": None
            }, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            if standard_id:
                standard = get_object_or_404(models.Standards, id=standard_id)
            else:
                standard = get_object_or_404(models.Standards, slug=slug)
            
            children = standard.children.all().order_by('number')
            serializer = StandardsListSerializer(children, many=True, context={'request': request})
            
            return Response({
                "status": True,
                "data": serializer.data
            }, status=status.HTTP_200_OK)
            
        except models.Standards.DoesNotExist:
            return Response({
                "status": False,
                "message": "Standard not found",
                "data": None
            }, status=status.HTTP_404_NOT_FOUND)


class StandardsAncestorsView(APIView):
    """Get ancestors of a specific standard"""
    
    def post(self, request, *args, **kwargs):
        standard_id = request.data.get('standard_id', None)
        slug = request.data.get('slug', None)
        
        if not standard_id and not slug:
            return Response({
                "status": False,
                "message": "standard_id or slug is required",
                "data": None
            }, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            if standard_id:
                standard = get_object_or_404(models.Standards, id=standard_id)
            else:
                standard = get_object_or_404(models.Standards, slug=slug)
            
            ancestors = standard.get_ancestors()
            serializer = StandardsListSerializer(ancestors, many=True, context={'request': request})
            
            return Response({
                "status": True,
                "data": serializer.data
            }, status=status.HTTP_200_OK)
            
        except models.Standards.DoesNotExist:
            return Response({
                "status": False,
                "message": "Standard not found",
                "data": None
            }, status=status.HTTP_404_NOT_FOUND)


class StandardsSiblingsView(APIView):
    """Get siblings of a specific standard"""
    
    def post(self, request, *args, **kwargs):
        standard_id = request.data.get('standard_id', None)
        slug = request.data.get('slug', None)
        
        if not standard_id and not slug:
            return Response({
                "status": False,
                "message": "standard_id or slug is required",
                "data": None
            }, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            if standard_id:
                standard = get_object_or_404(models.Standards, id=standard_id)
            else:
                standard = get_object_or_404(models.Standards, slug=slug)
            
            siblings = standard.get_siblings().order_by('number')
            serializer = StandardsListSerializer(siblings, many=True, context={'request': request})
            
            return Response({
                "status": True,
                "data": serializer.data
            }, status=status.HTTP_200_OK)
            
        except models.Standards.DoesNotExist:
            return Response({
                "status": False,
                "message": "Standard not found",
                "data": None
            }, status=status.HTTP_404_NOT_FOUND)


class StandardsFilterOptionsView(APIView):
    """Get filter options for standards (clusters, group names, types)"""
    
    def get(self, request, *args, **kwargs):
        clusters = models.Standards.objects.values_list('cluster', flat=True).distinct().order_by('cluster')
        group_names = models.Standards.objects.values_list('group_name', flat=True).distinct().order_by('group_name')
        types = models.Standards.objects.values_list('type', flat=True).distinct().order_by('type')
        
        return Response({
            "status": True,
            "data": {
                "clusters": list(clusters),
                "group_names": list(group_names),
                "types": list(types)
            }
        }, status=status.HTTP_200_OK)


class StandardsForCourseView(APIView):
    """Get all standards for course creation/selection"""
    
    def get(self, request, *args, **kwargs):
        standards = models.Standards.objects.all().order_by('number', 'standard_name')
        serializer = StandardsListSerializer(standards, many=True, context={'request': request})
        
        return Response({
            "status": True,
            "data": serializer.data
        }, status=status.HTTP_200_OK)


class AnswerStatusListView(APIView):
    """Get all available answer statuses"""
    
    def get(self, request, *args, **kwargs):
        answer_statuses = models.AnswerStatus.objects.all().order_by('title')
        status_data = []
        for answer_status in answer_statuses:
            status_data.append({
                'id': answer_status.id,
                'title': answer_status.title,
                'slug': answer_status.slug
            })
        
        return Response({
            "status": True,
            "data": status_data
        }, status=status.HTTP_200_OK)


class CategoryByIscoCodeView(APIView):
    """
    Find category (or categories) and their courses using ISCO code stored on Category.isco_code
    """

    def post(self, request, *args, **kwargs):
        isco_code = request.data.get('isco_code', None)

        if not isco_code:
            return Response({
                "status": False,
                "message": "isco_code is required",
                "data": None
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Find categories with the given ISCO code
            categories = models.Category.objects.filter(isco_code=isco_code).order_by('display_order', 'title')

            if not categories.exists():
                return Response({
                    "status": False,
                    "message": f"No categories found with isco_code: {isco_code}",
                    "data": []
                }, status=status.HTTP_404_NOT_FOUND)

            # For each category, get its courses
            result = []
            for category in categories:
                courses_qs = category.courses.all().select_related('standard', 'user', 'organizer', 'category')
                courses_serializer = CourseListSerializer(courses_qs, many=True, context={'request': request})

                result.append({
                    "category": {
                        "id": category.id,
                        "title": category.title,
                        "slug": category.slug,
                        "logo": request.build_absolute_uri(category.logo.url) if category.logo else None,
                        "home_page": category.home_page,
                        "display_order": category.display_order,
                        "old_code": category.old_code,
                        "isco_code": category.isco_code,
                        "parent": category.parent_id,
                    },
                    "courses": courses_serializer.data,
                })

            return Response({
                "status": True,
                "message": f"Found {categories.count()} categories for isco_code: {isco_code}",
                "data": {
                    "isco_code": isco_code,
                    "categories_count": categories.count(),
                    "categories": result,
                }
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({
                "status": False,
                "message": f"An error occurred: {str(e)}",
                "data": None
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CoursesByOldStandardCodeView(APIView):
    """Find courses using کد استاندارد قدیم (old standard code)"""
    
    def post(self, request, *args, **kwargs):
        old_standard_code = request.data.get('old_standard_code', None)
        
        if not old_standard_code:
            return Response({
                "status": False,
                "message": "old_standard_code is required",
                "data": None
            }, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            # Find standards with the given old standard code
            standards = models.Standards.objects.filter(old_standard_code=old_standard_code)
            
            if not standards.exists():
                return Response({
                    "status": False,
                    "message": f"No standards found with old standard code: {old_standard_code}",
                    "data": []
                }, status=status.HTTP_404_NOT_FOUND)
            
            # Get all courses related to these standards
            courses = models.Course.objects.filter(standard__in=standards).select_related('standard', 'user', 'organizer', 'category')
            
            if not courses.exists():
                return Response({
                    "status": True,
                    "message": f"No courses found for old standard code: {old_standard_code}",
                    "data": {
                        "old_standard_code": old_standard_code,
                        "standards_found": standards.count(),
                        "courses": []
                    }
                }, status=status.HTTP_200_OK)
            
            # Serialize the courses
            serializer = CourseListSerializer(courses, many=True, context={'request': request})
            
            return Response({
                "status": True,
                "message": f"Found {courses.count()} courses for old standard code: {old_standard_code}",
                "data": {
                    "old_standard_code": old_standard_code,
                    "standards_found": standards.count(),
                    "courses_count": courses.count(),
                    "courses": serializer.data
                }
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({
                "status": False,
                "message": f"An error occurred: {str(e)}",
                "data": None
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class OldStandardCodeSuggestView(APIView):
    """API to get suggestions for category and title based on old standard code"""
    
    def post(self, request, *args, **kwargs):
        old_standard_code = request.data.get('old_standard_code', None)
        
        if not old_standard_code:
            return Response({
                "status": False,
                "message": "old_standard_code parameter is required",
                "data": None
            }, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            # Search for standards with this old code
            standards = models.Standards.objects.filter(
                old_standard_code__icontains=old_standard_code
            )[:10]  # Limit to 10 results
            
            if not standards.exists():
                return Response({
                    "status": True,
                    "message": "No standards found with this code",
                    "data": {
                        "suggestions": []
                    }
                }, status=status.HTTP_200_OK)
            
            suggestions = []
            for standard in standards:
                # Try to find matching category based on group_name or cluster
                category = None
                category_id = None
                
                if standard.group_name:
                    # Try to find category by group_name
                    category = models.Category.objects.filter(
                        title__icontains=standard.group_name
                    ).first()
                
                if not category and standard.cluster:
                    # Try to find category by cluster
                    category = models.Category.objects.filter(
                        title__icontains=standard.cluster
                    ).first()
                
                if category:
                    category_id = category.id
                
                suggestions.append({
                    "standard_id": standard.id,
                    "standard_name": standard.standard_name,
                    "group_name": standard.group_name,
                    "cluster": standard.cluster,
                    "old_standard_code": standard.old_standard_code,
                    "suggested_category_id": category_id,
                    "suggested_category_title": category.title if category else None,
                    "suggested_title": standard.standard_name,  # Use standard name as suggested title
                })
            
            return Response({
                "status": True,
                "data": {
                    "suggestions": suggestions
                }
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({
                "status": False,
                "message": f"An error occurred: {str(e)}",
                "data": None
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class SearchView(APIView):
    """Search API for courses and categories"""
    
    def post(self, request, *args, **kwargs):
        search_query = request.data.get('search', None)
        organization_id = request.data.get('organization_id', None)
        page = request.data.get('page', 1)
        page_size = request.data.get('page_size', 10)
        
        if not search_query:
            return Response({
                "status": False,
                "message": "search parameter is required",
                "data": None
            }, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            # Search in courses (title, excerpt, description)
            # فقط دوره‌های تایید شده و منتشر شده
            courses = models.Course.objects.filter(
                (Q(title__icontains=search_query) |
                Q(excerpt__icontains=search_query) |
                Q(description__icontains=search_query)),
                is_published=True,
                is_verified=True
            )

            # Optional filter by organization (organizer) if provided
            if organization_id:
                courses = courses.filter(organizer_id=organization_id)

            courses = courses.order_by('-create_date')
            
            # Search in categories (title)
            categories = models.Category.objects.filter(
                title__icontains=search_query
            ).order_by('-create_date')
            
            # Paginate courses
            total_courses = courses.count()
            start_index = (page - 1) * page_size
            end_index = start_index + page_size
            paginated_courses = courses[start_index:end_index]
            
            # Paginate categories
            total_categories = categories.count()
            paginated_categories = categories[start_index:end_index]
            
            # Serialize courses
            courses_serializer = CourseListSerializer(paginated_courses, many=True, context={'request': request})
            
            # Serialize categories
            categories_serializer = CategorySerializer(paginated_categories, many=True, context={'request': request})
            
            # Calculate pagination info
            courses_next_page = None
            courses_previous_page = None
            categories_next_page = None
            categories_previous_page = None
            
            if end_index < total_courses:
                courses_next_page = page + 1
            if page > 1:
                courses_previous_page = page - 1
                
            if end_index < total_categories:
                categories_next_page = page + 1
            if page > 1:
                categories_previous_page = page - 1
            
            return Response({
                "status": True,
                "data": {
                    "courses": {
                        "count": total_courses,
                        "next": courses_next_page,
                        "previous": courses_previous_page,
                        "page": page,
                        "page_size": page_size,
                        "results": courses_serializer.data
                    },
                    "categories": {
                        "count": total_categories,
                        "next": categories_next_page,
                        "previous": categories_previous_page,
                        "page": page,
                        "page_size": page_size,
                        "results": categories_serializer.data
                    }
                }
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({
                "status": False,
                "message": f"An error occurred: {str(e)}",
                "data": None
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
