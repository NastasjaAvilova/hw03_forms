import datetime

from django.shortcuts import render, get_object_or_404, redirect

from .models import Post, Group

LAST_POSTS = 10


def index(request):
    posts = Post.objects.select_related('author')[:LAST_POSTS]
    template = 'posts/index.html'
    context = {'posts': posts}

    return render(request, template, context)


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)

    posts = group.posts.all()[:LAST_POSTS]

    context = {
        'group': group,
        'posts': posts,
    }
    return render(request, 'posts/group_list.html', context)


def only_user_view(request):
    if not request.user.is_authenticated:

        return redirect('/auth/login/')


def profile(request, username):
    # Здесь код запроса к модели и создание словаря контекста
    context = {
    }
    return render(request, 'posts/profile.html', context)


def post_detail(request, post_id):
    # Здесь код запроса к модели и создание словаря контекста
    context = {
    }
    return render(request, 'posts/post_detail.html', context) 