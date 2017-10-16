from django.shortcuts import render, redirect

# Create your views here.
from .forms import PostForm, PostCommentForm
from .models import Post


def post_list(request):
    """
    모든 Post목록을 리턴
    template은 'post/post_list.html'사용
    :param request:
    :return:
    """
    comment = PostCommentForm(request.POST)

    if comment.is_valid():
        post = request.GET.get('post')
        print(post)
        new_comment = comment.save(commit=False)
        print(comment)

        # new_comment.post = 1
        # new_comment.save()
        # return redirect(post_list)
    posts = Post.objects.all()
    context = {
        'posts':posts,
        'comment':comment,
    }
    return render(request, 'post/post_list.html', context)

def post_create(request):
    """

    :param request:
    :return:
    """
    imageform = PostForm(request.POST, request.FILES,)
    if imageform.is_valid():
        new_image = imageform.save(commit=False)
        new_image.save()
        return redirect(post_list)
    context = {
        'imageform' : imageform,
    }
    return render(request, 'post/post_create.html', context)

