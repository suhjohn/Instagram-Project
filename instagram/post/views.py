from django.http import HttpResponse, Http404, HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from django.contrib.auth.models import User


# Create your views here.
from member.decorators import login_required
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

@login_required
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


def post_detail(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)
    comment_form = PostCommentForm()
    context = {
        'post': post,
        'comment_form': comment_form,

    }
    return render(request, 'post/post_detail.html', context)

@login_required
def post_like_toggle(request, post_pk):
    """
    post_pk 에 해당하는 Post가
    현재 로그인한 유저의 like_posts에 있다면 없애고
    like_posts에 없다면 추가
    :param request:
    :param post_pk:
    :return:
    """

    next_path = request.GET.get('next')
    post = get_object_or_404(Post, pk=post_pk)
    user = request.user
    filtered_like_posts = user.like_posts.filter(pk=post.pk)
    if filtered_like_posts.exists():
        user.like_posts.remove(post)
    else:
        user.like_posts.add(post)

    if next_path:
        return redirect(next_path)
    return redirect('post:post_detail', post_pk=post_pk)


class PostLikeAPIToggle(APIView):
    """
    View to list all users in the system.

    * Requires token authentication.
    * Only admin users are able to access this view.
    """
    authentication_classes = (authentication.SessionAuthentication,)
    permission_classes = (permissions.IsAdminUser,)
    def get(self, request, format=None):
        """
        Return a list of all users.
        """
        usernames = [user.username for user in User.objects.all()]
        return Response(usernames)


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

