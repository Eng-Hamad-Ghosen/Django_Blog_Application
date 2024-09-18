import random
from django.shortcuts import render, get_object_or_404
from django.http import Http404, HttpRequest
from django.http import HttpResponse
from .models import Post
from django.core.paginator import Paginator, EmptyPage
from django.views.generic import ListView
from. forms import EmailPostForm
from django.core.mail import send_mail
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

class Post_List(ListView):
    model = Post
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post/post_list.html'

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

def post_share(request, id):
    post = get_object_or_404(Post, id=id)
    sent =False
    post_url = request.build_absolute_uri(post.get_absolute_url())
    if request.method=='POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            subject = f"{form.cleaned_data['name']}  recommend your read {post.title}"
            message = f"Read {post.title} at {post_url} \n {form.cleaned_data['name'] }\'s comments: {form.cleaned_data['comments']}"
            try:
                send_mail(subject, message, 'from_your_account@gmail.com', [form.cleaned_data['to']],fail_silently=False)
            except:
                
                sent = True
    else:
        form = EmailPostForm()
    return render(request, 'blog/post/share.html', {'form':form, 'post':post, 'sent':sent, 'post_url':post_url})