from django.db import models

from account.models import User
from course.models import Course


class Chat(models.Model):
    title = models.CharField(max_length=100)
    source_user = models.ForeignKey('account.User', on_delete=models.CASCADE, null=True, blank=True,
                                    related_name='source_user')
    destination_user = models.ForeignKey('account.User', on_delete=models.CASCADE, null=True, blank=True,
                                         related_name='destination_user')
    course = models.ForeignKey('course.Course', on_delete=models.CASCADE, related_name='course', blank=True, null=True)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Message(models.Model):
    chat = models.ForeignKey('Chat', on_delete=models.CASCADE, related_name='messages')
    user = models.ForeignKey('account.User', on_delete=models.CASCADE, related_name='user')
    content = models.TextField()
    file = models.FileField(upload_to='messages', null=True, blank=True)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.content
