from django import forms
from django.test import Client, TestCase
from django.urls import reverse

from posts.models import Group, Post, User

HOMEPAGE_URL = reverse('index')
NEW_POST_URL = reverse('new_post')
LOGIN_URL = reverse('login') + '?next='
TEST_USERNAME = 'mike'
POST_ID_KEY = 'post_id'
POSTID_VAL = 1
USERNAME_KEY = 'username'
POST_EDIT_URL = reverse(
    'post_edit', kwargs={USERNAME_KEY: TEST_USERNAME, POST_ID_KEY: POSTID_VAL})
POST_TEXT = 'Проверка создание поста'
FORM_TEXT = 'Текст из формы'
FORM_DATA_TEXT = 'text'
NOT_AUTH_USER = 'пользователь не авторизован'
TEST_TITLE = 'test-title'
TEST_SLUG = 'test-slug'
TEST_DESCRIPTION = 'test-description'


class PostCreateForm(TestCase):
    """Форма для создания поста."""
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.form = PostCreateForm()
        cls.user = User.objects.create_user(TEST_USERNAME)
        cls.gpoup = Group.objects.create(
            title=TEST_TITLE,
            slug=TEST_SLUG,
            description=TEST_DESCRIPTION)
        cls.post = Post.objects.create(
            text=POST_TEXT,
            author=cls.user,
            group=cls.gpoup)

    def setUp(self):
        self.guest_client = Client()
        # тут авторизованый пользователь
        self.user = PostCreateForm.user
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_new_post_no_auth(self):
        """Попытка создания поста не автор-ым пользователем"""
        keys_posts = list(Post.objects.values_list('id'))
        posts_count = Post.objects.count()
        form_data = {
            FORM_DATA_TEXT: FORM_TEXT,
            'author': self.user}
        response = self.guest_client.post(
            NEW_POST_URL,
            data=form_data,
            follow=True)
        self.assertRedirects(
            response,
            (LOGIN_URL + NEW_POST_URL))
        self.assertEqual(Post.objects.count(), posts_count)
        self.assertEqual(list(Post.objects.values_list('id')), keys_posts)

    def test_create_post(self):
        """Попытка создания поста автором"""
        posts_count = Post.objects.count()
        form_data = {
            FORM_DATA_TEXT: FORM_TEXT,
            'author': self.user,
            'group': self.gpoup.id}
        response = self.authorized_client.post(
            NEW_POST_URL,
            data=form_data,
            follow=True)
        self.assertRedirects(response, HOMEPAGE_URL)
        self.assertEqual(Post.objects.count(), posts_count + 1)
        self.assertEqual(self.post.author, self.user)
        self.assertEqual(self.post.group.id, form_data.get('group'))

    def test_context(self):
        """Правильный контекст для post_edit/new_post"""
        urls = NEW_POST_URL, POST_EDIT_URL
        form_filed = {
            'text': forms.fields.CharField,
            'group': forms.fields.ChoiceField
        }
        for check_url in urls:
            response = self.authorized_client.get(
                check_url, data=form_filed, follow=True)
            for name, form in form_filed.items():
                with self.subTest(name=name):
                    form_field = response.context['form'].fields[name]
                    self.assertIsInstance(form_field, form)

    def test_edit_post(self):
        """Проверка редактирования поста"""
        response_get = self.authorized_client.get(POST_EDIT_URL)
        data_get = response_get.context['form'].fields
        data_get['text'] = 'Измененный текст поста'
        self.authorized_client.post(
            POST_EDIT_URL,
            data=data_get,
            follow=True)
        response = self.authorized_client.get(POST_EDIT_URL)
        self.assertNotEqual(
            response.context['form'].initial['text'], 'Измененный текст поста')
