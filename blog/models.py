from django.db import models
from django.utils import timezone
from datetime import datetime
from django.contrib.auth.models import User
from django.urls import reverse
from taggit.managers import TaggableManager


# Create your models here.
class Post(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'DR, Draft'#choice = value, label
        PUBLISHED = 'PUB, Published'
    
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='auther_post')
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique_for_date='publish',blank=True, null=True)
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.DRAFT)
    
    tags = TaggableManager()
    
    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['-publish']
        indexes = [models.Index(fields=['title','publish'])]
    def get_absolute_url(self):
        # from django.core.urlresolvers import reverse
        return reverse('blog:post_details', kwargs={'slug': self.slug,
                                                    'year':self.publish.year,
                                                    'month':self.publish.month,
                                                    'day':self.publish.day})
        # return reverse('blog:post_details', args=[self.slug,
        #                                             self.publish.year,
        #                                             self.publish.month,
        #                                             self.publish.day])

class Comment(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='post_comment')
    
    name = models.CharField(max_length=50)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['created']
        indexes = [models.Index(fields=['created']),]
    def __str__(self):
        return f"Comment by {self.name} on {self.post}"
