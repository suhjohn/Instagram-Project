from django.shortcuts import render

# Create your views here.
from post.models import Post


def post_list(request):
    """
    모든 Post목록을 리턴
    template은 'post/post_list.html'사용
    :param request:
    :return:
    """

    posts = Post.objects.all()
    context = {
        'posts':posts,
    }
    return render(request, 'post/post_list.html', context)