from django.test import Client, TestCase

from posts.models import Group, Post, User

TEST_USERNAME = 'mike'
TEST_SLUG = 'test-slug'
TEST_TEXT = 'test-text'
TEST_TITLE = 'test-title'
TEST_DESCRIPTION = 'test-description'


class URLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(TEST_USERNAME)
        cls.gpoup = Group.objects.create(
            title=TEST_TITLE,
            slug=TEST_SLUG,
            description=TEST_DESCRIPTION)

    def setUp(self):
        """Создаем пользователя"""
        self.guest_client = Client()
        # тут авторизованый пользователь
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_homepage(self):
        """Страница / доступна любому пользователю."""
        response = self.guest_client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_group_slug(self):
        """Страница /group/<slug>/ доступна любому пользователю."""
        response = self.guest_client.get('/group/test-slug/')
        self.assertEqual(response.status_code, 200)

    def test_new_post(self):
        """Страница /new/ доступна авторизованному пользователю."""
        response = self.authorized_client.get('/new/')
        self.assertEqual(response.status_code, 200)
