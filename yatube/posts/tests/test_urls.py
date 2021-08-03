from django.test import Client, TestCase
from django.urls import reverse

from posts.models import Group, Post, User

TEST_USERNAME = 'mike'
TEST_SLUG = 'test-slug'
TEST_TEXT = 'test-text'
TEST_TITLE = 'test-title'
TEST_DESCRIPTION = 'test-description'
HOMEPAGE_URL = reverse('index')
NEW_POST_URL = reverse('new_post')
PROFILE_URL = reverse('profile', kwargs={'username': TEST_USERNAME})
GROUP_URL = reverse('group_posts', kwargs={'slug': TEST_SLUG})
LOG = reverse('login') + '?next='
POST_ID_KEY = 'post_id'
POSTID_VAL = 1
USERNAME_KEY = 'username'


class URLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(TEST_USERNAME)
        cls.post = Post.objects.create(
            text=TEST_TEXT,
            author=cls.user)
        cls.gpoup = Group.objects.create(
            title=TEST_TITLE,
            slug=TEST_SLUG,
            description=TEST_DESCRIPTION)
        cls.POST_EDIT_URL = reverse('post_edit', kwargs={
            'username': cls.user.username,
            'post_id': cls.post.id})
        cls.POST_URL = reverse('post', kwargs={
            'username': cls.user.username,
            'post_id': cls.post.id})

    def setUp(self):
        """Создаем пользователя"""
        self.guest_client = Client()
        # тут авторизованый пользователь
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_url_status(self):
        urls = [
            [HOMEPAGE_URL, self.guest_client, 200],
            [NEW_POST_URL, self.authorized_client, 200],
            [PROFILE_URL, self.authorized_client, 200],
            [self.POST_URL, self.guest_client, 200],
            [self.POST_EDIT_URL, self.authorized_client, 200],
            [self.POST_EDIT_URL, self.guest_client, 302],
            [GROUP_URL, self.guest_client, 200],
            [self.POST_EDIT_URL, self.guest_client, 302]
        ]
        for adress, client, httpstatus in urls:
            with self.subTest(adress=adress, client=client):
                self.assertEqual(client.get(adress).status_code, httpstatus)

    def test_correct_template(self):
        templates_url_names = [
            [HOMEPAGE_URL, self.guest_client, 'index.html'],
            [GROUP_URL, self.guest_client, 'group.html'],
            [NEW_POST_URL, self.authorized_client, 'new_post.html'],
            [self.POST_EDIT_URL, self.authorized_client, 'new_post.html'],
            [self.POST_URL, self.guest_client, 'post.html'],
            [PROFILE_URL, self.guest_client, 'profile.html']
        ]
        for adress, client, template in templates_url_names:
            with self.subTest(adress=adress):
                self.assertTemplateUsed(client.get(adress), template)

    def test_correct_redirect(self):
        redirect = [
            [NEW_POST_URL, LOG + NEW_POST_URL, self.guest_client],
            [self.POST_EDIT_URL, LOG + self.POST_EDIT_URL, self.guest_client],
            [self.POST_EDIT_URL, LOG + self.POST_EDIT_URL, self.guest_client]
        ]
        for adress, redirection, client in redirect:
            with self.subTest(adress=adress):
                self.assertRedirects(client.get(adress), redirection)
