import random
from django.shortcuts import render, get_object_or_404
from django.http import Http404
from django.http import HttpResponse
from .models import Post
from django.core.paginator import Paginator, EmptyPage
# Create your views here.

def post_list(request):
    posts = Post.objects.all()
    paginator = Paginator(posts,3)
    page_number = request.GET.get('page')
    try:
        posts = paginator.get_page(page_number)
    except EmptyPage:
        posts = paginator.get_page(paginator.page_number)
    return render(request,'blog/post/post_list.html', {'posts':posts})

def post_details(request, year, month, day, slug):
#method 1
    # try:
    #     post = Post.objects.grt(id=id)
    # except Post.DoesNotExist:
    #     raise Http404('No post found')
    # return render(request, 'post_details.html', {'post':post})

#method 2
    post = get_object_or_404(Post,
                             slug=slug,
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)
    return render(request, 'blog/post/post_details.html', {'post':post})