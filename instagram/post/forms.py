from django import forms

from .models import Post, PostComment


class PostForm(forms.ModelForm):
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['author'].required = True

    class Meta:
        model = Post
        fields = [
            "photo",
        ]


class PostCommentForm(forms.ModelForm):
    content = forms.CharField(
        label='',
    )

    class Meta:
        model = PostComment
        fields = [
            "content",
        ]

        # def is_valid(self):
        # self.instance.post
        # return super(PostCommentForm, self).form_valid()
