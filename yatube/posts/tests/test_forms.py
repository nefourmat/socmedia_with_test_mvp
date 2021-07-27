from django import forms
from django.test import Client
from django.urls import reverse

from posts.models import Post


class TaskCreateForm(forms.ModelForm):
    """Форма для создания поста."""
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.post = Post.objects.create(
            text='Проверка создание поста')

    def setUp(self):
        self.guest_client = Client()

    def test_new_post(self):
        posts_count = Post.objects.count()
        form_data = {
            'text': 'Текст из формы'
        }
        response = self.guest_client.post(
            reverse('new_post'),
            data=form_data,
            follow=True
        )
        self.assertEqual(Post.objects.count(), posts_count)
        self.assertFormError(
            response, 'text', 'пользователь не авторизован')
        self.assertEqual(response.status_code, 200)
