# Mahoverse E-Learning Platform - Seed Data

This document provides comprehensive seed data for the Mahoverse Django e-learning platform and instructions for its usage.

## 📋 Code Review Summary

### Project Structure
The Mahoverse project is a comprehensive e-learning platform built with Django and Django REST Framework, consisting of 5 main apps:

1. **Account App** - User management, authentication, roles, and permissions
2. **Course App** - Course management, lessons, tasks, and learning content
3. **Payment App** - Order processing and payment management
4. **Ticket App** - Support chat system
5. **Webinar App** - Live webinar management

### Key Features
- ✅ Custom user authentication with phone number
- ✅ Role-based access control (RBAC)
- ✅ Course management with chapters and lessons
- ✅ Task assignment and grading system
- ✅ Payment processing
- ✅ Support ticket system
- ✅ Webinar management
- ✅ Rating and review system
- ✅ Wishlist functionality
- ✅ File upload capabilities

### Technical Stack
- **Backend**: Django 5.1.3, Django REST Framework
- **Database**: MySQL
- **Authentication**: JWT tokens
- **File Handling**: Django Cleanup
- **CORS**: django-cors-headers

## 🚀 Seed Data Features

### Created Data Includes:

#### 1. **Geographic Data**
- 5 provinces (Tehran, Isfahan, Fars, Khorasan Razavi, East Azerbaijan)
- 25 cities across these provinces

#### 2. **User Management**
- **Roles**: مدیر کل (Super Admin), مدیر (Admin), استاد (Teacher), دانشجو (Student)
- **Permissions**: 20 different permissions covering all app functionalities
- **Users**: 10 sample users with different roles
- **Organizers**: 5 educational organizations

#### 3. **Course System**
- **Categories**: 5 parent categories with 30 child categories (all in Farsi)
  - برنامه‌نویسی (Programming)
  - طراحی (Design)
  - کسب و کار (Business)
  - زبان‌ها (Languages)
  - فناوری (Technology)
- **Courses**: 8 comprehensive courses across different subjects
- **Chapters**: 4 chapters per course (Introduction, Fundamentals, Advanced Topics, Projects)
- **Lessons**: 2 lessons per chapter
- **Tasks**: 3 difficulty levels (Beginner, Intermediate, Advanced)

#### 4. **Supporting Data**
- **Payment Statuses**: 6 status types
- **Transaction Situations**: 5 situation types
- **Answer Statuses**: 5 status types for task submissions
- **Learning Steps**: 6 step types
- **Webinars**: 3 sample webinars with topics

#### 5. **Sample Relationships**
- Course enrollments
- Course ratings and reviews
- Teacher-organizer assignments
- Sample comments

## 📦 Installation and Usage

### Prerequisites
- Python 3.8+
- Django 5.1.3
- MySQL database
- All dependencies from `requirements.txt`

### Quick Start

1. **Clone and setup the project**:
```bash
git clone <repository-url>
cd Mahoverse-2
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

2. **Configure database**:
```bash
# Update settings.py with your database credentials
python manage.py makemigrations
python manage.py migrate
```

3. **Run seed data**:
```bash
# Option 1: Using management command (Recommended)
python manage.py seed_data

# Option 2: Using the seed script directly
python manage.py shell < seed_data.py

# Option 3: Clear existing data and recreate
python manage.py seed_data --clear
```

### Default Credentials

#### Super Admin (مدیر کل)
- **Phone**: 09120000001
- **Email**: admin@mahoverse.ir
- **Password**: 12345678

#### Sample Users
- **Teachers (استاد)**: 09120000004, 09120000005, 09120000006
- **Students (دانشجو)**: 09120000007, 09120000008, 09120000009, 09120000010
- **Admins (مدیر)**: 09120000002, 09120000003
- **Organizer Users**: 09120001000, 09120001001, 09120001002, 09120001003, 09120001004

All users have the password: `12345678`

### Important Notes

#### File Fields
- **Organizer Logos**: The seed data creates dummy PNG files for organizer logos. In production, replace these with actual logo files.
- **Course Images**: Course images are optional and will be empty by default.
- **User Images**: User profile images are optional and will be empty by default.

#### Database Requirements
- The seed data requires a PostgreSQL or MySQL database
- Make sure all migrations are applied before running the seed data
- The script handles required fields like user assignments for organizers

## 📊 Data Structure Overview

### Account Models
```python
User (Custom user model with phone authentication)
├── Role (RBAC roles)
├── Permission (System permissions)
├── RolePermission (Role-permission relationships)
├── Province (Geographic data)
├── City (Geographic data)
├── Zone (Geographic data)
├── Organizer (Educational organizations)
└── OrganizerTeacher (Teacher-organization relationships)
```

### Course Models
```python
Course (Main course entity)
├── Category (Course categories with hierarchy)
├── Chapter (Course chapters)
├── Lesson (Course lessons)
├── Task (Assignments)
├── TaskAnswer (Student submissions)
├── Rate (Course ratings)
├── Comment (Course reviews)
├── WishList (User wishlists)
├── File (Course materials)
└── Session (Learning sessions)
```

### Payment Models
```python
Order (Purchase orders)
├── CourseOrder (Order items)
├── Transaction (Payment transactions)
├── Status (Order statuses)
└── Situation (Transaction situations)
```

### Support Models
```python
Chat (Support conversations)
└── Message (Chat messages)
```

### Webinar Models
```python
Webinar (Live webinars)
└── WebinarTopic (Webinar content)
```

## 🔧 Customization

### Adding More Data

1. **Add new courses**:
```python
# In the create_courses method
courses_data.append({
    'title': 'Your Course Title',
    'excerpt': 'Course summary',
    'description': 'Detailed description',
    'price': 1000000,
    'discount': 200000,
    'category': 'Existing Category Name',
    'organizer': 'Existing Organizer Name'
})
```

2. **Add new users**:
```python
# In the create_users method
users_data.append({
    'phone_number': '09120000011',
    'email': 'newuser@example.com',
    'first_name': 'New',
    'last_name': 'User',
    'role': student_role,
    'city': tehran,
    'gender': 'M'
})
```

3. **Add new categories**:
```python
# In the create_categories method
categories_data.append({
    'title': 'New Category',
    'children': ['Subcategory 1', 'Subcategory 2']
})
```

### Modifying Existing Data

Edit the respective methods in `account/management/commands/seed_data.py` to modify:
- User information
- Course details
- Pricing
- Categories
- Permissions

## 🧪 Testing the Data

### API Testing
```bash
# Start the development server
python manage.py runserver

# Test endpoints (examples)
curl http://localhost:8000/api/courses/
curl http://localhost:8000/api/users/
curl http://localhost:8000/api/categories/
```

### Admin Interface
```bash
# Access Django admin
http://localhost:8000/admin/

# Login with super admin credentials
Username: admin@mahoverse.ir
Password: 12345678
```

## 🔒 Security Considerations

### Production Deployment
- Change default passwords
- Update SECRET_KEY in settings.py
- Configure proper database credentials
- Set DEBUG=False
- Configure ALLOWED_HOSTS
- Use HTTPS
- Implement proper CORS settings

### Data Privacy
- Remove or anonymize personal data before production
- Review and update privacy policies
- Implement data retention policies

## 📝 Code Quality Notes

### Strengths
- ✅ Well-structured Django project
- ✅ Proper model relationships
- ✅ Role-based access control
- ✅ Comprehensive e-learning features
- ✅ File upload handling
- ✅ RESTful API design

### Recommendations
- 🔄 Add more comprehensive validation
- 🔄 Implement caching for better performance
- 🔄 Add comprehensive test coverage
- 🔄 Consider using Django signals for automation
- 🔄 Add API documentation (e.g., drf-spectacular)
- 🔄 Implement rate limiting
- 🔄 Add logging and monitoring

## 🐛 Troubleshooting

### Common Issues

1. **Database connection errors**:
   - Check database credentials in settings.py
   - Ensure MySQL service is running
   - Verify database exists

2. **Migration errors**:
   ```bash
   python manage.py makemigrations --merge
   python manage.py migrate
   ```

3. **Permission errors**:
   - Ensure proper file permissions
   - Check media directory exists

4. **Import errors**:
   - Verify all dependencies are installed
   - Check Python path

### Getting Help
- Check Django documentation
- Review Django REST Framework docs
- Check project logs for detailed error messages

## 📄 License

This seed data is provided for development and testing purposes. Please ensure compliance with your project's licensing requirements.

---

**Note**: This seed data creates a comprehensive testing environment. For production use, ensure all data is properly reviewed and sanitized according to your security requirements. 