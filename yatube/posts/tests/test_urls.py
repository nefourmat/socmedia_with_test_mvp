from django.contrib.auth import get_user_model
from django.test import Client, TestCase

from posts.models import Group, Post

User = get_user_model()


class URLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user('mike')
        cls.post = Post.objects.create(
            text='test-text',
            author=cls.user
        )
        cls.gpoup = Group.objects.create(
            title='test-title',
            slug='test-slug',
            description='test-description')

    def setUp(self):
        """Создаем пользователя"""
        self.guest_client = Client()
        # тут авторизованый пользователь
        self.user = URLTests.user
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

    def test_profile(self):
        """Страница /profile/ доступна любому пользователю."""
        response = self.guest_client.get('/mike/')
        self.assertEqual(response.status_code, 200)

    def test_profile_post(self):
        """Страница /profile/<post_id> доступна любому пользователю."""
        response = self.guest_client.get('/mike/1/')
        self.assertEqual(response.status_code, 200)

    def test_profile_post_edit(self):
        """Страница редактирования поста доступна только автору"""
        if self.post.author == self.user:
            response = self.authorized_client.get('/mike/1/edit/')
            self.assertEqual(response.status_code, 200)

    def test_redirect_no_author(self):
        """Перенаправляет тех, у кого нет прав доступа к этой странице."""
        response = self.guest_client.get('/mike/1/edit/')
        self.assertEqual(response.status_code, 302)

    def test_templates(self):
        """URL-адрес использует соответствующий шаблон."""
        templates_url_names = {
            'index.html': '/',
            'group.html': '/group/test-slug/',
            'new_post.html': '/new/',
            'new_post.html': '/mike/1/edit/'
        }
        for template, adress in templates_url_names.items():
            with self.subTest(adress=adress):
                response = self.authorized_client.get(adress)
                self.assertTemplateUsed(response, template)
