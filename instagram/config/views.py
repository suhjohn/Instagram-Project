from django.shortcuts import redirect


def landing_page(request):
    if request.user.is_authenticated:
        return redirect('post:post_list')
    return redirect('member:login')