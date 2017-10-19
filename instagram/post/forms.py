from django import forms

from .models import Post, PostComment


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            "photo",
        ]


class PostCommentForm(forms.ModelForm):
    content = forms.CharField(
        label='',
        widget=forms.Textarea(
            attrs={
                'placeholder': '댓글 달기..',

            }
        )
    )

    class Meta:
        model = PostComment
        fields = [
            "content",
        ]

        # def is_valid(self):
        # self.instance.post
        # return super(PostCommentForm, self).form_valid()
