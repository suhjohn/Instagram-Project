from django.http import HttpResponse, Http404, HttpResponseForbidden
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
    if bool(request.user.is_authenticated):
        comment_form = PostCommentForm()
        posts = Post.objects.all()
        context = {
            'posts': posts,
            'comment_form': comment_form,
        }
        return render(request, 'post/post_list.html', context)
    return redirect('member:login')


def post_create(request):
    """

    :param request:
    :return:
    """
    if bool(request.user.is_authenticated):
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.author = request.user
            new_post.save()
            return redirect('post:post_list')
        context = {
            'imageform': form,
        }
        return render(request, 'post/post_create.html', context)
    else:
        return redirect('member:login')


def post_delete(request, post_pk):
    next = request.GET.get('next', '').strip()
    post = get_object_or_404(Post, pk=post_pk)
    if post.author == request.user:
        post.delete()
        return redirect(next)
    else:
        return HttpResponseForbidden()


def add_comment(request, post_pk):
    if bool(request.user.is_authenticated):
        post = Post.objects.get(pk=post_pk)
        comment = PostCommentForm(request.POST)
        next = request.GET.get('next', '').strip()
        if comment.is_valid():
            new_comment = comment.save(commit=False)
            new_comment.author = request.user
            new_comment.post = post
            new_comment.save()
        return redirect(next)
    else:
        return redirect('member:login')


def delete_comment(request, comment_pk):
    next = request.GET.get('next', '').strip()
    comment = get_object_or_404(PostComment, pk=comment_pk)
    if comment.author == request.user:
        comment.delete()
        return redirect(next)
    else:
        return HttpResponseForbidden()


def post_detail(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)
    comment_form = PostCommentForm()
    context = {
        'post': post,
        'comment_form': comment_form,

    }
    return render(request, 'post/post_detail.html', context)
