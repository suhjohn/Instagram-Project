from django.contrib.auth import authenticate
from django.test import TestCase, TransactionTestCase

# Create your tests here.
from member.views import User


class UserModelTest(TransactionTestCase):
    DUMMY_USERNAME = 'username'
    DUMMY_PASSWORD = 'password'
    DUMMY_AGE = 0

    def test_fields_default_value(self):
        """
        default값이 잘 들어가 있나 확인 - 쓸데없는 값이 안들어가있는지 확인
        :return:
        """
        user = User.objects.create_user(
            username=self.DUMMY_USERNAME,
            password=self.DUMMY_PASSWORD,
            age=self.DUMMY_AGE,
        )
        self.assertEqual(user.first_name, '')
        self.assertEqual(user.last_name, '')
        self.assertEqual(user.username, self.DUMMY_USERNAME)
        self.assertEqual(user.img_profile, '')
        self.assertEqual(user.age, self.DUMMY_AGE)
        self.assertEqual(user.following_users.count(), 0)

        # 입력한 username, psasword로 인증한 user와 위에서 생성한 user가 같은지
        self.assertEqual(user, authenticate(
            username=self.DUMMY_USERNAME,
            password=self.DUMMY_PASSWORD,
        ))

    def test_follow(self):
        mina, hyeri, yura, sojin = [User.objects.create(
            username=f'username{i}',
            age=0) for name in ['민아', '혜리', '유라', '소진']]
        mina.follow_toggle(hyeri)
        mina.follow_toggle(yura)
        mina.follow_toggle(sojin)

        hyeri.follow_toggle(yura)
        hyeri.follow_toggle(sojin)

        yura.follow_toggle(sojin)

        members = [mina, hyeri, yura, sojin]

        for user, count in zip(members, [3, 2, 1, 0]):
            self.assertEqual(user.fllowing_users.count(), count)
        # self.assertEqual(mina.following_users.count(), 3)
        # self.assertEqual(hyeri.following_users.count(), 2)
        # self.assertEqual(yura.following_users.count(), 1)
        # self.assertEqual(sojin.following_users.count(), 0)

        self.assertIn(hyeri, mina.following_users.all())
        self.assertIn(yura, mina.following_users.all())
        self.assertIn(sojin, mina.following_users.all())

        self.assertIn(mina, hyeri.following_users.all())
        self.assertIn(mina, yura.following_users.all())
        self.assertIn(mina, sojin.following_users.all())

