from django.shortcuts import render, get_object_or_404, redirect

from .models import Post, Group, User

from .forms import PostForm


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
    template = 'posts/profile.html'
    author = get_object_or_404(User, username=username)
    # Здесь код запроса к модели и создание словаря контекста
    context = {'author': author}
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
    if request.user != post.author:
        return redirect('posts:post_detail', post_id)
    form = PostForm(request.POST or None)
    if form.is_valid():
        post.save()
        return redirect('posts:post_detail', post_id,)
    is_edit = True
    context = {'form': form, 'is_edit': is_edit}
    return render(request, template, context)
