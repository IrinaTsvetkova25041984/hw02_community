from django.shortcuts import render, get_object_or_404
from .models import Post, Group


def index(request):
    posts = Post.objects.order_by('-pub_date')[:10]
    context = {
        'posts': posts,
    }
    return render(request, 'posts/index.html', context)

def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    posts = Post.objects.filter(group=group).order_by('-pub_date')[:10]
    context = {
        'group': group,
        'posts': posts,
    }
    return render(request, 'posts/group_list.html', context)

def base(request):
    template = 'posts/base.html'
    return render(request, template)

def header(request):
    template = 'includes/header.html'
    return render(request, template)

def footer(request):
    template = 'includes/footer.html'
    return render(request, template)

