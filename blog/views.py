from django.shortcuts import render, get_object_or_404
from django.http import Http404
from django.http import HttpResponse
from .models import Post
# Create your views here.

def post_list(request):
    posts = Post.objects.all()
    return render(request,'blog/post/post_list.html', {'posts':posts})

def post_details(request, id):
#method 1
    # try:
    #     post = Post.objects.grt(id=id)
    # except Post.DoesNotExist:
    #     raise Http404('No post found')
    # return render(request, 'post_details.html', {'post':post})

#method 2
    post = get_object_or_404(Post, id=id)
    return render(request, 'blog/post/post_details.html', {'post':post})