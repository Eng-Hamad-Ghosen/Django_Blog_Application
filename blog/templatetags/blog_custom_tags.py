from django import template
from ..models import Post, Comment
from django.db.models import Count
register = template.Library()

@register.simple_tag
def total_posts():
    return Post.objects.count()


@register.inclusion_tag('blog/post/latest_posts.html')
def show_latest_posts(count=5):
    latest_posts = Post.objects.order_by('-publish')[:count]
    return {'latest_posts': latest_posts}

# @register.simple_tag
# def show_more_comments():
#     all_posts = Post.objects.annotate(total_comments=Count('post_comment')).order_by('-total_comments')
#     return {'more_comments':all_posts}

@register.simple_tag
def get_most_commented_posts(count=5):
    
    return Post.objects.annotate(total_comments=Count('post_comment')).order_by('-total_comments')[:count]
