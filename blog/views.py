import random
from django.shortcuts import render, get_object_or_404
from django.http import Http404, HttpRequest
from django.http import HttpResponse
from .models import Post, Comment
from django.core.paginator import Paginator, EmptyPage
from django.views.generic import ListView
from. forms import EmailPostForm, CommentForm
from django.core.mail import send_mail
from django.views.decorators.http import require_POST
from taggit.models import Tag
from django.db.models import Count

# Create your views here.

def post_list(request, tag_slug=None):
    posts = Post.objects.all()
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        posts = posts.filter(tags__in=[tag])
    paginator = Paginator(posts,3)
    page_number = request.GET.get('page')
    try:
        posts = paginator.get_page(page_number)
    except EmptyPage:
        posts = paginator.get_page(paginator.page_number)
    return render(request,'blog/post/post_list.html', {'posts':posts, 'tag':tag})

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
    comment_count = Comment.objects.filter(post=post).count()
    
    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.objects.filter(tags__in=post_tags_ids).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags','-publish')
    print(post_tags_ids)
    print(similar_posts)
    return render(request, 'blog/post/post_details.html', {'post':post, 'comment_count':comment_count, 'similar_posts':similar_posts})

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

# @require_POST
def post_comment(request, id):
    post = get_object_or_404(Post, id=id)
    comments = Comment.objects.filter(post=post)
    comment = None
    if request.method=='POST':
        form = CommentForm(data=request.POST)
        if form.is_valid():
            obj_comment = form.save(commit=False)
            obj_comment.post = post
            obj_comment.save()
            comment = 'Done'
            return render(request, 'blog/post/comment.html', {'post':post,
                                                        'form':form,
                                                        'comment':comment,
                                                        'comments':comments})
    form = CommentForm()
    return render(request, 'blog/post/comment.html', {'post':post,
                                                    'form':form,
                                                    'comment':comment,
                                                    'comments':comments})


