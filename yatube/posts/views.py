from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404


from .models import Group, Post, User
from .forms import PostForm



def index(request):
    posts = Post.objects.select_related('group')[:settings.LIMIT_POSTS]
    post_list = Post.objects.all()
    paginator = Paginator(post_list, settings.LIMIT_POSTS)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'posts': posts,
        'page_obj': page_obj,
    }
    return render(request, 'posts/index.html', context)


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    posts = Post.objects.select_related('group')[:settings.LIMIT_POSTS]
    post_list = Post.objects.all()
    paginator = Paginator(post_list, settings.LIMIT_POSTS)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'group': group,
        'page_obj': page_obj,
    }
    return render(request, 'posts/group_list.html', context)


def user_contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['body']
            form.save()
        return redirect('/thank-you/')
    return render(request, 'contact.html', {'form': form})
    form = ContactForm()
    return render(request, 'users/contact.html', {'form': form})


def profile(request, username):
    author = get_object_or_404(User, username=username)
    post_list = author.post.all()
    posts = Post.objects.all()
    paginator = Paginator(post_list, settings.LIMIT_POSTS)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    post_number = post_list.count()
    context = {
        'author': author,
        'posts': posts,
        'page_obj': page_obj,
    }
    return render(request, 'posts/profile.html', context)


def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    author_posts = post.author.post.all()
    context = {
        'post': post,
        'author_posts': author_posts.count(),
    }
    return render(request, 'posts/post_detail.html', context) 

@login_required
def post_create(request):
    form = PostForm(request.POST or None)
    if form.is_valid():
        post.author = request.user
        form.save()
        return redirect('posts:profile', username=request.user)
    return render(request, 'posts/post_create.html', {'form': form})

@login_required
def post_edit(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if post.author != request.user:
        return redirect('posts:post_detail', post_id=post_id)
    if form.is_valid():
        form.save()
        return redirect('posts:post_detail', post_id=post_id)
    return render(request, 'posts/post_create.html', {'form': form, 'post': post})
