from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Group, User
from django.conf import settings
from .forms import PostForm


def index(request):
    posts = Post.objects.all()
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
    }
    return render(request, 'posts/index.html', context)


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    posts = group.posts.all()[:settings.POSTS_COUNT]
    context = {
        'group': group,
        'posts': posts
    }
    return render(request, 'posts/group_list.html', context)


def profile(request, username):
    author = get_object_or_404(User, username=username)
    post_list = author.posts.all()
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    posts_count = author.posts.count()
    context = {
        'author': author,
        'page_obj': page_obj,
        'posts': post_list,
        'posts_count': posts_count,
    }
    return render(request, 'posts/profile.html', context)


def post_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    posts_count = post.author.posts.count()
    title = post.text[0:30]
    context = {
        'post': post,
        'posts_count': posts_count,
        'title': title,
    }
    return render(request, 'posts/post_detail.html', context)


@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST or None)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('posts:profile', post.author.username)
    form = PostForm()
    return render(request, 'posts/post_create.html', {'form': form})


def post_edit(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    is_edit = True
    form = PostForm(request.POST, instance=post)
    if form.is_valid():
        post.save()
        return redirect('posts:post_detail', post_id)
    context = {
        'is_edit': is_edit,
        'form': form,
    }
    return render(request, 'posts/post_create.html', context)
