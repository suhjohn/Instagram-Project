from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from .forms import PostForm, PostCommentForm
from .models import Post, PostComment


def post_list(request):
    """
    모든 Post목록을 리턴
    template은 'post/post_list.html'사용
    :param request:
    :return:
    """
    comment_form = PostCommentForm()
    posts = Post.objects.all()
    context = {
        'posts': posts,
        'comment_form': comment_form,
    }
    return render(request, 'post/post_list.html', context)


def post_create(request):
    """

    :param request:
    :return:
    """
    print(request)
    imageform = PostForm(request.POST, request.FILES)
    if imageform.is_valid():
        new_image = imageform.save(commit=False)
        new_image.save()
        return redirect('post:post_list')
    context = {
        'imageform': imageform,
    }
    return render(request, 'post/post_create.html', context)


def add_comment(request, post_pk):
    post = Post.objects.get(pk=post_pk)
    comment = PostCommentForm(request.POST)
    if comment.is_valid():
        PostComment.objects.create(
            post=post,
            content=comment.cleaned_data['content']
        )
    return redirect('post:post_list')


def delete_comment(request, pk):
    post = Post.objects.get(pk=pk)


def post_detail(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)

    comment_form = PostCommentForm()
    context = {
        'post': post,
        'comment_form': comment_form,

    }
    return render(request, 'post/post_detail.html', context)

