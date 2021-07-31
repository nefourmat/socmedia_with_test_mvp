from django import forms
from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from posts.models import Post

User = get_user_model()

HOMEPAGE_URL = reverse('index')
NEW_POST_URL = reverse('new_post')
LOGIN_URL = reverse('login') + '?next='
POST_EDIT_URL = reverse('post_edit', kwargs={'username': 'mike', 'post_id': 1})
TEST_USERNAME = 'mike'
POST_TEXT = 'Проверка создание поста'
FORM_TEXT = 'Текст из формы'
FORM_DATA_TEXT = 'text'
NOT_AUTH_USER = 'пользователь не авторизован'


class PostCreateForm(TestCase):
    """Форма для создания поста."""
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.form = PostCreateForm()
        cls.user = User.objects.create_user(TEST_USERNAME)
        cls.post = Post.objects.create(
            text=POST_TEXT,
            author=cls.user)

    def setUp(self):
        self.guest_client = Client()
        # тут авторизованый пользователь
        self.user = PostCreateForm.user
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_new_post_no_auth(self):
        """Попытка создания поста не автор-ым пользователем"""
        all_posts = list(Post.objects.values_list('id'))
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
        self.assertEqual(list(Post.objects.values_list('id')), all_posts)

    def test_create_post(self):
        """Попытка создания поста автором"""
        posts_count = Post.objects.count()
        form_data = {
            FORM_DATA_TEXT: FORM_TEXT,
            'author': self.user}
        response = self.authorized_client.post(
            NEW_POST_URL,
            data=form_data,
            follow=True)
        self.assertRedirects(response, HOMEPAGE_URL)
        self.assertEqual(Post.objects.count(), posts_count + 1)

    def test_edit(self):
        """Проверка редактирования поста"""
        post = Post.objects.create(
            text='edit',
            author=self.user)
        post_edit = Post.objects.filter(
            text='edit').update(text=('edit') + 'w')
        post.refresh_from_db()
        self.assertNotEqual(post, post_edit)

    def test_test(self):
        """Правильный контекст для post_edit/new_post"""
        urls = NEW_POST_URL, POST_EDIT_URL
        form_filed = {
            'text': forms.fields.CharField,
            'group': forms.fields.ChoiceField
        }
        for check_url in urls:
            response = self.authorized_client.get(check_url)
            for name, form in form_filed.items():
                with self.subTest(name=name):
                    form_field = response.context['form'].fields[name]
                    self.assertIsInstance(form_field, form)
