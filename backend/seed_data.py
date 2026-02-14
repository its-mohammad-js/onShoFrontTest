#!/usr/bin/env python
"""
Seed Data for Mahoverse E-Learning Platform
This script creates comprehensive seed data for all models in the project.
Run with: python manage.py shell < seed_data.py
"""

import os
import sys
import django
from datetime import datetime, timedelta
from django.utils import timezone
from django.core.files.images import ImageFile
from django.contrib.auth.hashers import make_password
from django.db import transaction

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Mahoverse.settings')
django.setup()

from account.models import (
    User, Role, Permission, RolePermission, Province, City, Zone,
    Organizer, OrganizerTeacher, UserOtp
)
from course.models import (
    Category, Course, Chapter, Lesson, File, Task, TaskAnswer,
    AnswerStatus, Rate, WishList, Comment, Step, Session,
    Attribute, AttributeValue, CourseAttribute, CategoryAttribute
)
from payment.models import Status, Order, CourseOrder, Situation, Transaction
from ticket.models import Chat, Message
from webinar.models import Webinar, WebinarTopic

def create_provinces_and_cities():
    """Create provinces and cities data"""
    print("Creating provinces and cities...")
    
    provinces_data = [
        {
            'title': 'Tehran',
            'cities': ['Tehran', 'Shahriar', 'Varamin', 'Firoozkooh', 'Damavand']
        },
        {
            'title': 'Isfahan',
            'cities': ['Isfahan', 'Kashan', 'Najafabad', 'Shahreza', 'Golpayegan']
        },
        {
            'title': 'Fars',
            'cities': ['Shiraz', 'Marvdasht', 'Jahrom', 'Kazerun', 'Fasa']
        },
        {
            'title': 'Khorasan Razavi',
            'cities': ['Mashhad', 'Nishapur', 'Sabzevar', 'Kashmar', 'Torbat-e Heydarieh']
        },
        {
            'title': 'East Azerbaijan',
            'cities': ['Tabriz', 'Maragheh', 'Marand', 'Ahar', 'Mianeh']
        }
    ]
    
    for province_data in provinces_data:
        province, created = Province.objects.get_or_create(
            title=province_data['title']
        )
        if created:
            print(f"Created province: {province.title}")
        
        for city_name in province_data['cities']:
            city, created = City.objects.get_or_create(
                title=city_name,
                province=province
            )
            if created:
                print(f"Created city: {city.title} in {province.title}")

def create_roles_and_permissions():
    """Create roles and permissions"""
    print("Creating roles and permissions...")
    
    # Create permissions
    permissions_data = [
        'course_create', 'course_edit', 'course_delete', 'course_view',
        'lesson_create', 'lesson_edit', 'lesson_delete', 'lesson_view',
        'user_manage', 'order_manage', 'payment_manage', 'webinar_manage',
        'ticket_manage', 'comment_manage', 'rating_manage', 'file_upload',
        'task_create', 'task_grade', 'task_view', 'chat_manage'
    ]
    
    permissions = {}
    for perm_slug in permissions_data:
        perm, created = Permission.objects.get_or_create(
            title=perm_slug.replace('_', ' ').title(),
            slug=perm_slug
        )
        permissions[perm_slug] = perm
        if created:
            print(f"Created permission: {perm.title}")
    
    # Create roles with Farsi names and slugs
    roles_data = [
        {
            'title': 'مدیر کل',
            'slug': 'مدیر-کل',
            'permissions': permissions.keys()
        },
        {
            'title': 'مدیر',
            'slug': 'مدیر',
            'permissions': [
                'course_create', 'course_edit', 'course_view', 'lesson_create',
                'lesson_edit', 'lesson_view', 'user_manage', 'order_manage',
                'payment_manage', 'webinar_manage', 'ticket_manage',
                'comment_manage', 'rating_manage', 'file_upload'
            ]
        },
        {
            'title': 'استاد',
            'slug': 'استاد',
            'permissions': [
                'course_create', 'course_edit', 'course_view', 'lesson_create',
                'lesson_edit', 'lesson_view', 'task_create', 'task_grade',
                'task_view', 'file_upload', 'comment_manage'
            ]
        },
        {
            'title': 'دانشجو',
            'slug': 'دانشجو',
            'permissions': [
                'course_view', 'lesson_view', 'task_view', 'comment_manage',
                'rating_manage'
            ]
        }
    ]
    
    for role_data in roles_data:
        role, created = Role.objects.get_or_create(
            title=role_data['title'],
            defaults={'slug': role_data['slug']}
        )
        if created:
            print(f"Created role: {role.title} (slug: {role.slug})")
        
        # Assign permissions to role
        for perm_slug in role_data['permissions']:
            if perm_slug in permissions:
                RolePermission.objects.get_or_create(
                    role=role,
                    permission=permissions[perm_slug]
                )

def create_organizers():
    """Create educational organizations"""
    print("Creating organizers...")
    
    organizers_data = [
        {
            'name': 'Tech Academy',
            'description': 'Leading technology education platform specializing in programming and software development.',
            'website_url': 'https://techacademy.ir'
        },
        {
            'name': 'Digital Learning Institute',
            'description': 'Comprehensive digital skills training center offering courses in design, marketing, and business.',
            'website_url': 'https://dli.ir'
        },
        {
            'name': 'Creative Arts Center',
            'description': 'Professional arts and design education with focus on graphic design, photography, and multimedia.',
            'website_url': 'https://creativearts.ir'
        },
        {
            'name': 'Business School Online',
            'description': 'Advanced business and management education for professionals and entrepreneurs.',
            'website_url': 'https://bso.ir'
        },
        {
            'name': 'Language Learning Hub',
            'description': 'Comprehensive language education platform offering courses in English, French, German, and more.',
            'website_url': 'https://llh.ir'
        }
    ]
    
    # Get admin role for organizer users
    admin_role = Role.objects.filter(title='مدیر').first()
    if not admin_role:
        print('No admin role found. Creating organizers without user assignment.')
        return
    
    # Get Tehran city for organizer users
    tehran = City.objects.filter(title='Tehran').first()
    if not tehran:
        print('No Tehran city found. Creating organizers without user assignment.')
        return
    
    for i, org_data in enumerate(organizers_data):
        # Check if organizer already exists
        if Organizer.objects.filter(name=org_data['name']).exists():
            print(f"Organizer {org_data['name']} already exists, skipping...")
            continue
        
        # Create a dedicated user for this organizer
        organizer_user_data = {
            'phone_number': f'0912000{1000 + i:04d}',  # 09120001000, 09120001001, etc.
            'email': f'organizer{i+1}@{org_data["name"].lower().replace(" ", "").replace("-", "")}.ir',
            'first_name': f'Organizer{i+1}',
            'last_name': 'Manager',
            'role': admin_role,
            'city': tehran,
            'gender': 'M' if i % 2 == 0 else 'F'
        }
        
        try:
            # Create organizer user
            organizer_user, created = User.objects.get_or_create(
                phone_number=organizer_user_data['phone_number'],
                defaults={
                    'email': organizer_user_data['email'],
                    'first_name': organizer_user_data['first_name'],
                    'last_name': organizer_user_data['last_name'],
                    'role': organizer_user_data['role'],
                    'city': organizer_user_data['city'],
                    'gender': organizer_user_data['gender'],
                    'password': make_password('12345678')
                }
            )
            
            if created:
                print(f"Created organizer user: {organizer_user.first_name} {organizer_user.last_name}")
            
            # Create organizer with the dedicated user
            from django.core.files.base import ContentFile
            
            # Create a simple dummy image file
            dummy_image_content = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x02\x00\x00\x00\x90wS\xde\x00\x00\x00\tpHYs\x00\x00\x0b\x13\x00\x00\x0b\x13\x01\x00\x9a\x9c\x18\x00\x00\x00\x0cIDATx\x9cc```\x00\x00\x00\x04\x00\x01\xf5\'\x04\xf6\x00\x00\x00\x00IEND\xaeB`\x82'
            
            organizer = Organizer.objects.create(
                user=organizer_user,
                name=org_data['name'],
                description=org_data['description'],
                website_url=org_data['website_url']
            )
            
            # Add dummy logo
            logo_filename = f'organizer_{i+1}.png'
            organizer.logo.save(logo_filename, ContentFile(dummy_image_content), save=True)
            
            print(f"Created organizer: {organizer.name} assigned to {organizer_user.first_name}")
            
        except Exception as e:
            print(f"Error creating organizer {org_data['name']}: {e}")
            continue

def create_users():
    """Create users with different roles"""
    print("Creating users...")
    
    # Get roles
    super_admin_role = Role.objects.get(title='مدیر کل')
    admin_role = Role.objects.get(title='مدیر')
    teacher_role = Role.objects.get(title='استاد')
    student_role = Role.objects.get(title='دانشجو')
    
    # Get cities
    tehran = City.objects.get(title='Tehran')
    isfahan = City.objects.get(title='Isfahan')
    shiraz = City.objects.get(title='Shiraz')
    
    users_data = [
        # Super Admin
        {
            'phone_number': '09120000001',
            'email': 'admin@mahoverse.ir',
            'first_name': 'Admin',
            'last_name': 'System',
            'role': super_admin_role,
            'city': tehran,
            'gender': 'M',
            'is_staff': True,
            'is_superuser': True
        },
        # Admins
        {
            'phone_number': '09120000002',
            'email': 'manager@techacademy.ir',
            'first_name': 'Ahmad',
            'last_name': 'Mohammadi',
            'role': admin_role,
            'city': tehran,
            'gender': 'M'
        },
        {
            'phone_number': '09120000003',
            'email': 'director@dli.ir',
            'first_name': 'Fatemeh',
            'last_name': 'Ahmadi',
            'role': admin_role,
            'city': isfahan,
            'gender': 'F'
        },
        # Teachers
        {
            'phone_number': '09120000004',
            'email': 'teacher1@techacademy.ir',
            'first_name': 'Ali',
            'last_name': 'Karimi',
            'role': teacher_role,
            'city': tehran,
            'gender': 'M'
        },
        {
            'phone_number': '09120000005',
            'email': 'teacher2@dli.ir',
            'first_name': 'Sara',
            'last_name': 'Hosseini',
            'role': teacher_role,
            'city': isfahan,
            'gender': 'F'
        },
        {
            'phone_number': '09120000006',
            'email': 'teacher3@creativearts.ir',
            'first_name': 'Reza',
            'last_name': 'Naderi',
            'role': teacher_role,
            'city': shiraz,
            'gender': 'M'
        },
        # Students
        {
            'phone_number': '09120000007',
            'email': 'student1@example.com',
            'first_name': 'Mohammad',
            'last_name': 'Rahimi',
            'role': student_role,
            'city': tehran,
            'gender': 'M'
        },
        {
            'phone_number': '09120000008',
            'email': 'student2@example.com',
            'first_name': 'Zahra',
            'last_name': 'Salehi',
            'role': student_role,
            'city': isfahan,
            'gender': 'F'
        },
        {
            'phone_number': '09120000009',
            'email': 'student3@example.com',
            'first_name': 'Hassan',
            'last_name': 'Mirzaei',
            'role': student_role,
            'city': shiraz,
            'gender': 'M'
        },
        {
            'phone_number': '09120000010',
            'email': 'student4@example.com',
            'first_name': 'Narges',
            'last_name': 'Kazemi',
            'role': student_role,
            'city': tehran,
            'gender': 'F'
        }
    ]
    
    for user_data in users_data:
        user, created = User.objects.get_or_create(
            phone_number=user_data['phone_number'],
            defaults={
                'email': user_data['email'],
                'first_name': user_data['first_name'],
                'last_name': user_data['last_name'],
                'role': user_data['role'],
                'city': user_data['city'],
                'gender': user_data['gender'],
                'is_staff': user_data.get('is_staff', False),
                'is_superuser': user_data.get('is_superuser', False),
                'password': make_password('12345678')
            }
        )
        if created:
            print(f"Created user: {user.first_name} {user.last_name}")

def create_organizer_teachers():
    """Create organizer-teacher relationships"""
    print("Creating organizer-teacher relationships...")
    
    organizers = Organizer.objects.all()
    teachers = User.objects.filter(role__title='استاد')
    
    for i, teacher in enumerate(teachers):
        organizer = organizers[i % len(organizers)]
        OrganizerTeacher.objects.get_or_create(
            user=teacher,
            organization=organizer
        )
        print(f"Assigned {teacher.first_name} to {organizer.name}")

def create_categories():
    """Create course categories"""
    print("Creating categories...")
    
    categories_data = [
        {
            'title': 'برنامه‌نویسی',
            'slug': 'برنامه-نویسی',
            'children': [
                {'title': 'برنامه‌نویسی پایتون', 'slug': 'برنامه-نویسی-پایتون'},
                {'title': 'توسعه جاوااسکریپت', 'slug': 'توسعه-جاوااسکریپت'},
                {'title': 'برنامه‌نویسی جاوا', 'slug': 'برنامه-نویسی-جاوا'},
                {'title': 'برنامه‌نویسی ++C', 'slug': 'برنامه-نویسی-++c'},
                {'title': 'توسعه وب', 'slug': 'توسعه-وب'},
                {'title': 'توسعه موبایل', 'slug': 'توسعه-موبایل'}
            ]
        },
        {
            'title': 'طراحی',
            'slug': 'طراحی',
            'children': [
                {'title': 'طراحی گرافیک', 'slug': 'طراحی-گرافیک'},
                {'title': 'طراحی رابط کاربری', 'slug': 'طراحی-رابط-کاربری'},
                {'title': 'طراحی وب', 'slug': 'طراحی-وب'},
                {'title': 'طراحی لوگو', 'slug': 'طراحی-لوگو'},
                {'title': 'تایپوگرافی', 'slug': 'تایپوگرافی'},
                {'title': 'هنر دیجیتال', 'slug': 'هنر-دیجیتال'}
            ]
        },
        {
            'title': 'کسب و کار',
            'slug': 'کسب-و-کار',
            'children': [
                {'title': 'بازاریابی دیجیتال', 'slug': 'بازاریابی-دیجیتال'},
                {'title': 'مدیریت پروژه', 'slug': 'مدیریت-پروژه'},
                {'title': 'کارآفرینی', 'slug': 'کارآفرینی'},
                {'title': 'استراتژی کسب و کار', 'slug': 'استراتژی-کسب-و-کار'},
                {'title': 'مدیریت مالی', 'slug': 'مدیریت-مالی'},
                {'title': 'رهبری', 'slug': 'رهبری'}
            ]
        },
        {
            'title': 'زبان‌ها',
            'slug': 'زبان-ها',
            'children': [
                {'title': 'انگلیسی', 'slug': 'انگلیسی'},
                {'title': 'فرانسوی', 'slug': 'فرانسوی'},
                {'title': 'آلمانی', 'slug': 'آلمانی'},
                {'title': 'اسپانیایی', 'slug': 'اسپانیایی'},
                {'title': 'عربی', 'slug': 'عربی'},
                {'title': 'فارسی برای خارجیان', 'slug': 'فارسی-برای-خارجیان'}
            ]
        },
        {
            'title': 'فناوری',
            'slug': 'فناوری',
            'children': [
                {'title': 'هوش مصنوعی', 'slug': 'هوش-مصنوعی'},
                {'title': 'یادگیری ماشین', 'slug': 'یادگیری-ماشین'},
                {'title': 'علم داده', 'slug': 'علم-داده'},
                {'title': 'امنیت سایبری', 'slug': 'امنیت-سایبری'},
                {'title': 'رایانش ابری', 'slug': 'رایانش-ابری'},
                {'title': 'بلاکچین', 'slug': 'بلاکچین'}
            ]
        }
    ]
    
    for parent_data in categories_data:
        parent, created = Category.objects.get_or_create(
            title=parent_data['title'],
            defaults={'slug': parent_data['slug']}
        )
        if created:
            print(f"Created parent category: {parent.title} (slug: {parent.slug})")
        
        for child_data in parent_data['children']:
            child, created = Category.objects.get_or_create(
                title=child_data['title'],
                parent=parent,
                defaults={'slug': child_data['slug']}
            )
            if created:
                print(f"Created child category: {child.title} (slug: {child.slug})")

def create_courses():
    """Create sample courses"""
    print("Creating courses...")
    
    # Get data
    teachers = User.objects.filter(role__title='استاد')
    organizers = Organizer.objects.all()
    categories = Category.objects.filter(parent__isnull=False)  # Only child categories
    
    courses_data = [
            {
                'title': 'Complete Python Bootcamp',
                'excerpt': 'Learn Python programming from scratch to advanced level',
                'description': 'This comprehensive course covers Python fundamentals, object-oriented programming, web development with Django, data analysis, and more. Perfect for beginners and intermediate developers.',
                'price': 1200000,
                'discount': 200000,
                'category': 'برنامه‌نویسی پایتون',
                'organizer': 'Tech Academy'
            },
            {
                'title': 'JavaScript Masterclass',
                'excerpt': 'Master JavaScript and modern web development',
                'description': 'Learn JavaScript ES6+, DOM manipulation, async programming, and modern frameworks like React and Node.js. Build real-world projects.',
                'price': 1500000,
                'discount': 300000,
                'category': 'توسعه جاوااسکریپت',
                'organizer': 'Tech Academy'
            },
            {
                'title': 'UI/UX Design Fundamentals',
                'excerpt': 'Learn the principles of user interface and user experience design',
                'description': 'Master the fundamentals of UI/UX design including wireframing, prototyping, user research, and design systems. Create beautiful and functional interfaces.',
                'price': 1800000,
                'discount': 400000,
                'category': 'طراحی رابط کاربری',
                'organizer': 'Digital Learning Institute'
            },
            {
                'title': 'Digital Marketing Strategy',
                'excerpt': 'Comprehensive digital marketing course for business growth',
                'description': 'Learn SEO, social media marketing, content marketing, email marketing, and analytics. Develop effective marketing strategies for your business.',
                'price': 2000000,
                'discount': 500000,
                'category': 'بازاریابی دیجیتال',
                'organizer': 'Business School Online'
            },
            {
                'title': 'Advanced English Conversation',
                'excerpt': 'Improve your English speaking and listening skills',
                'description': 'Practice real-world English conversations, improve pronunciation, expand vocabulary, and gain confidence in speaking English fluently.',
                'price': 800000,
                'discount': 100000,
                'category': 'انگلیسی',
                'organizer': 'Language Learning Hub'
            },
            {
                'title': 'Machine Learning Basics',
                'excerpt': 'Introduction to machine learning and artificial intelligence',
                'description': 'Learn the fundamentals of machine learning, algorithms, data preprocessing, and model evaluation. Build your first ML models.',
                'price': 2500000,
                'discount': 600000,
                'category': 'هوش مصنوعی',
                'organizer': 'Tech Academy'
            },
            {
                'title': 'Graphic Design Mastery',
                'excerpt': 'Master graphic design tools and principles',
                'description': 'Learn Adobe Photoshop, Illustrator, and InDesign. Master design principles, color theory, typography, and create professional designs.',
                'price': 1600000,
                'discount': 300000,
                'category': 'طراحی گرافیک',
                'organizer': 'Creative Arts Center'
            },
            {
                'title': 'Project Management Professional',
                'excerpt': 'Become a certified project manager',
                'description': 'Learn project management methodologies, tools, and best practices. Prepare for PMP certification and manage projects effectively.',
                'price': 2200000,
                'discount': 400000,
                'category': 'مدیریت پروژه',
                'organizer': 'Business School Online'
            }
        ]
    
    for i, course_data in enumerate(courses_data):
        teacher = teachers[i % len(teachers)]
        category = Category.objects.get(title=course_data['category'])
        organizer = Organizer.objects.get(name=course_data['organizer'])
        
        course, created = Course.objects.get_or_create(
            title=course_data['title'],
            defaults={
                'excerpt': course_data['excerpt'],
                'description': course_data['description'],
                'price': course_data['price'],
                'discount': course_data['discount'],
                'user': teacher,
                'category': category,
                'organizer': organizer,
                'mentor': teacher
            }
        )
        
        # Add course image if created
        if created:
            from django.core.files.base import ContentFile
            
            # Create a simple dummy image file for each course
            dummy_image_content = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x02\x00\x00\x00\x90wS\xde\x00\x00\x00\tpHYs\x00\x00\x0b\x13\x00\x00\x0b\x13\x01\x00\x9a\x9c\x18\x00\x00\x00\x0cIDATx\x9cc```\x00\x00\x00\x04\x00\x01\xf5\'\x04\xf6\x00\x00\x00\x00IEND\xaeB`\x82'
            
            image_filename = f'course_{i+1}.png'
            course.image.save(image_filename, ContentFile(dummy_image_content), save=True)
        if created:
            print(f"Created course: {course.title}")

def create_attributes_and_values():
    """Create attributes and their values"""
    print("Creating attributes and values...")
    
    attributes_data = [
        {
            'title': 'مدت زمان دوره',
            'type': 'text',
            'slug': 'duration',
            'values': ['20 ساعت', '25 ساعت', '30 ساعت', '35 ساعت', '40 ساعت', '45 ساعت', '50 ساعت']
        },
        {
            'title': 'تعداد موقعیت شغلی',
            'type': 'number',
            'slug': 'job_positions',
            'values': ['5', '8', '10', '12', '15', '20', '25', '30']
        },
        {
            'title': 'زبان برنامه‌نویسی',
            'type': 'text',
            'slug': 'language',
            'values': ['پایتون', 'جاوااسکریپت', 'HTML/CSS', 'React', 'Node.js', 'Django', 'Vue.js', 'Angular']
        },
        {
            'title': 'سطح دوره',
            'type': 'text',
            'slug': 'level',
            'values': ['مبتدی', 'متوسط', 'پیشرفته', 'حرفه‌ای']
        },
        {
            'title': 'پیش‌نیاز',
            'type': 'text',
            'slug': 'need',
            'values': ['بدون پیش‌نیاز', 'آشنایی اولیه با برنامه‌نویسی', 'آشنایی با HTML و CSS', 'آشنایی با پایتون', 'آشنایی با شبکه', 'تجربه در طراحی']
        },
        {
            'title': 'منتور',
            'type': 'text',
            'slug': 'mentor',
            'values': ['دکتر حسینی', 'مهندس رضایی', 'دکتر احمدی', 'مهندس کریمی', 'دکتر صادقی', 'مهندس محمدی']
        },
        {
            'title': 'زبان آموزش',
            'type': 'text',
            'slug': 'teaching_language',
            'values': ['فارسی', 'انگلیسی', 'ترکی', 'آلمانی']
        }
    ]
    
    for attr_data in attributes_data:
        attribute, created = Attribute.objects.get_or_create(
            title=attr_data['title'],
            defaults={
                'type': attr_data['type'],
                'slug': attr_data['slug']
            }
        )
        if created:
            print(f"Created attribute: {attribute.title}")
            
            # Create attribute values
            for value_text in attr_data['values']:
                AttributeValue.objects.get_or_create(
                    attribute=attribute,
                    value=value_text
                )
            print(f"Created {len(attr_data['values'])} values for {attribute.title}")

def create_course_attributes():
    """Create course attributes for all courses"""
    print("Creating course attributes...")
    
    courses = Course.objects.all()
    
    # Define course-specific attributes
    course_attributes_map = {
        'Complete Python Bootcamp': {
            'مدت زمان دوره': '30 ساعت',
            'تعداد موقعیت شغلی': '15',
            'زبان برنامه‌نویسی': 'پایتون',
            'سطح دوره': 'مبتدی',
            'پیش‌نیاز': 'بدون پیش‌نیاز',
            'منتور': 'دکتر حسینی',
            'زبان آموزش': 'فارسی'
        },
        'JavaScript Masterclass': {
            'مدت زمان دوره': '25 ساعت',
            'تعداد موقعیت شغلی': '12',
            'زبان برنامه‌نویسی': 'جاوااسکریپت',
            'سطح دوره': 'متوسط',
            'پیش‌نیاز': 'آشنایی اولیه با برنامه‌نویسی',
            'منتور': 'مهندس رضایی',
            'زبان آموزش': 'فارسی'
        },
        'UI/UX Design Fundamentals': {
            'مدت زمان دوره': '20 ساعت',
            'تعداد موقعیت شغلی': '10',
            'زبان برنامه‌نویسی': 'HTML/CSS',
            'سطح دوره': 'مبتدی',
            'پیش‌نیاز': 'آشنایی با HTML و CSS',
            'منتور': 'مهندس کریمی',
            'زبان آموزش': 'فارسی'
        },
        'Digital Marketing Strategy': {
            'مدت زمان دوره': '35 ساعت',
            'تعداد موقعیت شغلی': '20',
            'زبان برنامه‌نویسی': 'متفرقه',
            'سطح دوره': 'متوسط',
            'پیش‌نیاز': 'بدون پیش‌نیاز',
            'منتور': 'دکتر احمدی',
            'زبان آموزش': 'فارسی'
        },
        'Advanced English Conversation': {
            'مدت زمان دوره': '40 ساعت',
            'تعداد موقعیت شغلی': '8',
            'زبان برنامه‌نویسی': 'متفرقه',
            'سطح دوره': 'متوسط',
            'پیش‌نیاز': 'آشنایی اولیه با انگلیسی',
            'منتور': 'مهندس محمدی',
            'زبان آموزش': 'انگلیسی'
        },
        'Machine Learning Basics': {
            'مدت زمان دوره': '45 ساعت',
            'تعداد موقعیت شغلی': '5',
            'زبان برنامه‌نویسی': 'پایتون',
            'سطح دوره': 'پیشرفته',
            'پیش‌نیاز': 'آشنایی با پایتون',
            'منتور': 'دکتر صادقی',
            'زبان آموزش': 'فارسی'
        },
        'Graphic Design Mastery': {
            'مدت زمان دوره': '30 ساعت',
            'تعداد موقعیت شغلی': '12',
            'زبان برنامه‌نویسی': 'متفرقه',
            'سطح دوره': 'متوسط',
            'پیش‌نیاز': 'تجربه در طراحی',
            'منتور': 'مهندس کریمی',
            'زبان آموزش': 'فارسی'
        },
        'Project Management Professional': {
            'مدت زمان دوره': '35 ساعت',
            'تعداد موقعیت شغلی': '18',
            'زبان برنامه‌نویسی': 'متفرقه',
            'سطح دوره': 'متوسط',
            'پیش‌نیاز': 'بدون پیش‌نیاز',
            'منتور': 'دکتر احمدی',
            'زبان آموزش': 'فارسی'
        }
    }
    
    for course in courses:
        course_attrs = course_attributes_map.get(course.title, {})
        
        for attr_title, attr_value in course_attrs.items():
            try:
                attribute = Attribute.objects.get(title=attr_title)
                CourseAttribute.objects.get_or_create(
                    course=course,
                    attribute=attribute,
                    defaults={'value': attr_value}
                )
            except Attribute.DoesNotExist:
                print(f"Attribute '{attr_title}' not found for course '{course.title}'")
                continue
        
        print(f"Created attributes for course: {course.title}")

def create_chapters_and_lessons():
    """Create chapters and lessons for courses"""
    print("Creating chapters and lessons...")
    
    courses = Course.objects.all()
    
    for course in courses:
        # Create chapters
        chapter_data = [
            {
                'title': 'Introduction',
                'lessons': [
                    {
                        'title': 'Welcome to the Course',
                        'content': f'Welcome to {course.title}! In this lesson, we will introduce you to the course structure and what you will learn.'
                    },
                    {
                        'title': 'Course Overview',
                        'content': 'This lesson provides an overview of the topics covered in this course and the learning objectives.'
                    }
                ]
            },
            {
                'title': 'Fundamentals',
                'lessons': [
                    {
                        'title': 'Basic Concepts',
                        'content': 'Learn the fundamental concepts and principles that form the foundation of this subject.'
                    },
                    {
                        'title': 'Getting Started',
                        'content': 'Step-by-step guide to get you started with the practical aspects of this course.'
                    }
                ]
            },
            {
                'title': 'Advanced Topics',
                'lessons': [
                    {
                        'title': 'Advanced Techniques',
                        'content': 'Explore advanced techniques and methodologies used by professionals in this field.'
                    },
                    {
                        'title': 'Best Practices',
                        'content': 'Learn industry best practices and standards to ensure high-quality results.'
                    }
                ]
            },
            {
                'title': 'Projects and Applications',
                'lessons': [
                    {
                        'title': 'Real-World Projects',
                        'content': 'Apply your knowledge to real-world projects and case studies.'
                    },
                    {
                        'title': 'Final Project',
                        'content': 'Complete a comprehensive final project that demonstrates your mastery of the subject.'
                    }
                ]
            }
        ]
        
        for i, chapter_info in enumerate(chapter_data):
            chapter, created = Chapter.objects.get_or_create(
                title=chapter_info['title'],
                course=course,
                defaults={'order': i + 1}
            )
            if created:
                print(f"Created chapter: {chapter.title} for {course.title}")
            
            for j, lesson_info in enumerate(chapter_info['lessons']):
                lesson, created = Lesson.objects.get_or_create(
                    title=lesson_info['title'],
                    chapter=chapter,
                    course=course,
                    defaults={'content': lesson_info['content']}
                )
                if created:
                    print(f"Created lesson: {lesson.title}")

def create_tasks():
    """Create tasks for lessons"""
    print("Creating tasks...")
    
    lessons = Lesson.objects.all()
    teachers = User.objects.filter(role__title='استاد')
    
    task_data = [
        {
            'title': 'Assignment 1: Basic Exercise',
            'description': 'Complete the basic exercise to demonstrate your understanding of the fundamental concepts.',
            'difficulty': 'beginner'
        },
        {
            'title': 'Assignment 2: Intermediate Project',
            'description': 'Create an intermediate-level project that showcases your practical skills.',
            'difficulty': 'intermediate'
        },
        {
            'title': 'Assignment 3: Advanced Challenge',
            'description': 'Tackle this advanced challenge to test your mastery of the subject.',
            'difficulty': 'advanced'
        }
    ]
    
    for i, lesson in enumerate(lessons):
        if i % 3 == 0:  # Create task for every 3rd lesson
            task_info = task_data[i % len(task_data)]
            teacher = teachers[i % len(teachers)]
            
            task, created = Task.objects.get_or_create(
                title=task_info['title'],
                lesson=lesson,
                defaults={
                    'description': task_info['description'],
                    'mentor': teacher,
                    'difficulty': task_info['difficulty']
                }
            )
            if created:
                print(f"Created task: {task.title}")

def create_answer_statuses():
    """Create answer statuses"""
    print("Creating answer statuses...")
    
    statuses = [
        'Pending Review',
        'Under Review',
        'Approved',
        'Needs Revision',
        'Rejected'
    ]
    
    for status_title in statuses:
        status, created = AnswerStatus.objects.get_or_create(title=status_title)
        if created:
            print(f"Created answer status: {status.title}")

def create_steps():
    """Create learning steps"""
    print("Creating steps...")
    
    steps = [
        'Introduction',
        'Theory',
        'Practice',
        'Review',
        'Assessment',
        'Feedback'
    ]
    
    for step_title in steps:
        step, created = Step.objects.get_or_create(title=step_title)
        if created:
            print(f"Created step: {step.title}")

def create_payment_statuses():
    """Create payment statuses"""
    print("Creating payment statuses...")
    
    statuses = [
        'Pending',
        'Processing',
        'Completed',
        'Failed',
        'Cancelled',
        'Refunded'
    ]
    
    for status_title in statuses:
        status, created = Status.objects.get_or_create(title=status_title)
        if created:
            print(f"Created payment status: {status.title}")

def create_situations():
    """Create transaction situations"""
    print("Creating transaction situations...")
    
    situations = [
        'Successful',
        'Failed',
        'Pending',
        'Cancelled',
        'Refunded'
    ]
    
    for situation_title in situations:
        situation, created = Situation.objects.get_or_create(title=situation_title)
        if created:
            print(f"Created transaction situation: {situation.title}")

def create_webinars():
    """Create sample webinars"""
    print("Creating webinars...")
    
    webinars_data = [
        {
            'title': 'Future of AI in Education',
            'description': 'Explore how artificial intelligence is transforming education and what the future holds.',
            'speaker': 'Dr. Ali Rezaei',
            'date': '2024-03-15',
            'start_time': '14:00',
            'end_time': '16:00',
            'price': 500000,
            'is_free': False
        },
        {
            'title': 'Digital Marketing Trends 2024',
            'description': 'Learn about the latest trends in digital marketing and how to implement them.',
            'speaker': 'Sara Hosseini',
            'date': '2024-03-20',
            'start_time': '15:00',
            'end_time': '17:00',
            'price': 0,
            'is_free': True
        },
        {
            'title': 'Web Development Best Practices',
            'description': 'Discover the best practices for modern web development and optimization.',
            'speaker': 'Mohammad Karimi',
            'date': '2024-03-25',
            'start_time': '16:00',
            'end_time': '18:00',
            'price': 300000,
            'is_free': False
        }
    ]
    
    for webinar_data in webinars_data:
        webinar, created = Webinar.objects.get_or_create(
            title=webinar_data['title'],
            defaults={
                'description': webinar_data['description'],
                'speaker': webinar_data['speaker'],
                'date': webinar_data['date'],
                'start_time': webinar_data['start_time'],
                'end_time': webinar_data['end_time'],
                'price': webinar_data['price'],
                'is_free': webinar_data['is_free']
            }
        )
        if created:
            print(f"Created webinar: {webinar.title}")
            
            # Create webinar topics
            topics = [
                {
                    'title': 'Introduction and Overview',
                    'content': 'Introduction to the webinar topic and overview of what will be covered.'
                },
                {
                    'title': 'Main Discussion',
                    'content': 'In-depth discussion of the main topics and concepts.'
                },
                {
                    'title': 'Q&A Session',
                    'content': 'Question and answer session with participants.'
                }
            ]
            
            for topic_data in topics:
                topic, created = WebinarTopic.objects.get_or_create(
                    webinar=webinar,
                    title=topic_data['title'],
                    defaults={'content': topic_data['content']}
                )
                if created:
                    print(f"Created webinar topic: {topic.title}")

def create_sample_data():
    """Create sample data for testing"""
    print("Creating sample data...")
    
    # Create some course enrollments
    students = User.objects.filter(role__title='دانشجو')
    courses = Course.objects.all()
    
    for i, student in enumerate(students):
        course = courses[i % len(courses)]
        from course.models import CourseUser
        enrollment, created = CourseUser.objects.get_or_create(
            course=course,
            user=student,
            defaults={'status': 'in_progress'}
        )
        if created:
            print(f"Enrolled {student.first_name} in {course.title}")
    
    # Create some ratings
    for i, student in enumerate(students):
        course = courses[i % len(courses)]
        rate, created = Rate.objects.get_or_create(
            user=student,
            course=course,
            defaults={'rate': 4 + (i % 2)}  # 4 or 5 stars
        )
        if created:
            print(f"Created rating: {rate.rate} stars for {course.title}")
    
    # Create some comments
    comments_data = [
        "دوره بسیار عالی! محتوا کامل و ساختاریافته است.",
        "مدرس مفاهیم را به وضوح توضیح می‌دهد. بسیار توصیه می‌کنم!",
        "محتوای عالی و مثال‌های عملی مفید.",
        "این دوره به من کمک کرد مهارت‌هایم را به طور قابل توجهی بهبود دهم.",
        "دوره خوبی است، اما می‌تواند موضوعات پیشرفته‌تری داشته باشد.",
        "کیفیت آموزش بسیار بالا و مدرس تجربه‌ای عالی دارد.",
        "مطالب به روز و کاربردی هستند. برای شروع کار عالی است.",
        "پروژه‌های عملی دوره بسیار مفید بودند.",
        "دوره‌ای جامع که همه جنبه‌های موضوع را پوشش می‌دهد.",
        "توصیه می‌کنم این دوره را حتماً بگذرانید."
    ]
    
    for i, comment_text in enumerate(comments_data):
        student = students[i % len(students)]
        course = courses[i % len(courses)]
        comment, created = Comment.objects.get_or_create(
            content=comment_text,
            user=student,
            course=course
        )
        if created:
            print(f"Created comment by {student.first_name}")

def main():
    """Main function to run all seed data creation"""
    print("Starting seed data creation...")
    
    try:
        with transaction.atomic():
            create_provinces_and_cities()
            create_roles_and_permissions()
            create_organizers()
            create_users()
            create_organizer_teachers()
            create_categories()
            create_courses()
            create_attributes_and_values()
            create_course_attributes()
            create_chapters_and_lessons()
            create_tasks()
            create_answer_statuses()
            create_steps()
            create_payment_statuses()
            create_situations()
            create_webinars()
            create_sample_data()
            
        print("\n✅ Seed data creation completed successfully!")
        print("\nSummary:")
        print(f"- {Province.objects.count()} provinces")
        print(f"- {City.objects.count()} cities")
        print(f"- {User.objects.count()} users")
        print(f"- {Role.objects.count()} roles")
        print(f"- {Permission.objects.count()} permissions")
        print(f"- {Organizer.objects.count()} organizers")
        print(f"- {Category.objects.count()} categories")
        print(f"- {Course.objects.count()} courses")
        print(f"- {Chapter.objects.count()} chapters")
        print(f"- {Lesson.objects.count()} lessons")
        print(f"- {Task.objects.count()} tasks")
        print(f"- {Webinar.objects.count()} webinars")
        
    except Exception as e:
        print(f"❌ Error creating seed data: {e}")
        raise

if __name__ == '__main__':
    main() 