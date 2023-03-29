from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from .models import Post, Group, User
from .forms import PostForm
from .utils import get_page_context


last_posts = 10


def index(request):
    template = 'posts/index.html'
    posts = Post.objects.all()
    context = {'page_obj': get_page_context(posts, request, last_posts)}

    return render(request, template, context)


def group_posts(request, slug):
    template = 'posts/group_list.html'
    group = get_object_or_404(Group, slug=slug)
    posts = group.posts.all()
    context = {
        'group': group,
        'page_obj': get_page_context(posts, request, last_posts),
    }
    return render(request, template, context)


def only_user_view(request):
    if not request.user.is_authenticated:

        return redirect('/auth/login/')


def profile(request, username):
    template = 'posts/profile.html'
    author = get_object_or_404(User, username=username)
    posts = author.posts.select_related('author').all()
    context = {
        'author': author,
        'page_obj': get_page_context(posts, request, last_posts),
    }
    return render(request, template, context)


def post_detail(request, post_id):
    template = 'posts/post_detail.html'
    post = get_object_or_404(Post, id=post_id)
    context = {'post': post}
    return render(request, template, context)


def post_create(request):
    template = 'posts/create_post.html'
    form = PostForm(request.POST or None)
    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.save()
        return redirect('posts:profile', post.author)
    context = {'form': form}
    return render(request, template, context)


def post_edit(request, post_id):
    template = 'posts/create_post.html'
    post = get_object_or_404(Post, id=post_id)
    is_edit = True
    form = PostForm(request.POST or None, instance=post)
    if post.author != request.user:
        return redirect('posts:index')
    if form.is_valid():
        form.save()
        return redirect('posts:post_detail', post_id=post.id)
    context = {
        'form': form,
        'is_edit': is_edit,
        'post': post,
    }
    return render(request, template, context)
