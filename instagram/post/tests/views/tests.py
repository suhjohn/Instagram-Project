from pydoc import resolve
from unittest import TestCase

from django.urls import reverse

from ... import views


class PostLikeToggleViewTest(TestCase):
    TEST_POST_PK = 37
    VIEW_URL = f'/post/{TEST_POST_PK}/like'
    VIEW_URL_NAME = 'post:post_like_toggle'

    def test_url_equal_reverse_url_name(self):
        self.assertEqual(self.VIEW_URL, reverse(self.VIEW_URL_NAME, kwargs={'post_pk': self.TEST_POST_PK}))

    def test_url_resolves_to_post_like_toggle_view(self):
        """
        VIEW_URL_NAME을 reverse한, 또는 VIEW_URL자체에 해당하는 view가 실제 views.post_like_toggle 뷰를 가리키는지 테스트
        :return:
        """
        found = resolve(self.VIEW_URL)
        self.assertEqual(found.func, views.post_like_toggle)