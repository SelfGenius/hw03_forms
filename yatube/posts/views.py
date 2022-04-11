from django.conf import settings
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, render, redirect
from django.utils import timezone

from .forms import PostForm
from .models import Group, Post, User


def index(request):
    post_list = Post.objects.select_related('author', 'group')
    paginator = Paginator(post_list, settings.NUMBER_OF_ENTRIES)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    title = 'Последние обновления на сайте'
    context = {
        'page_obj': page_obj,
        'title': title,
    }
    return render(request, 'posts/index.html', context)


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    post_list = group.posts.select_related('author')
    paginator = Paginator(post_list, settings.NUMBER_OF_ENTRIES)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'group': group,
        'page_obj': page_obj,
    }
    return render(request, 'posts/group_list.html', context, )


def profile(request, username):
    user = get_object_or_404(User, username=username)
    post_list = user.posts.all()
    count_post = post_list.count()
    paginator = Paginator(post_list, settings.NUMBER_OF_ENTRIES)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
        'count_post': count_post,
        'author': user,
    }
    return render(request, 'posts/profile.html', context)


def post_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    user = get_object_or_404(User, username=post.author)
    count_post = user.posts.filter(author=user).count()
    context = {
        'post': post,
        'count_post': count_post,
    }
    return render(request, 'posts/post_detail.html', context)


def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('posts:profile', username=post.author)
    else:
        form = PostForm()

    return render(request, 'posts/create_post.html', {'form': form})


def post_edit(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('posts:post_detail', post_id=post_id)
    else:
        form = PostForm(instance=post)
    return render(request, 'posts/create_post.html',
                  {'form': form, 'is_edit': True})
