from django.db import models
from django.utils import timezone
from datetime import datetime
from django.contrib.auth.models import User
# Create your models here.
class Post(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'DR, Draft'#choice = value, label
        PUBLISHED = 'PUB, Published'
    
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='auther_post')
    title = models.CharField(max_length=250)
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.DRAFT)
    slug = models.SlugField(max_length=250 ,blank=True, null=True)
    
    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['-publish']
        indexes = [models.Index(fields=['title','publish'])]
