from django import forms
from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from posts.models import Group, Post

User = get_user_model()


class ViewsTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user('mike')
        cls.gpoup = Group.objects.create(
            title='test-title',
            slug='test-slug',
            description='test-description'
        )
        cls.post = Post.objects.create(
            text='test-text',
            author=ViewsTests.user)

    def setUp(self):
        """Создаем пользователя"""
        self.guest_client = Client()
        self.user = ViewsTests.user
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_pages_use_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        templates_pages_names = {
            'index.html': reverse('index'),
            'new_post.html': reverse('new_post'),
            'group.html': (
                reverse('group_posts', kwargs={'slug': 'test-slug'})
            ),
        }
        for template, reverse_name in templates_pages_names.items():
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template)

    def test_pages_use_correct_templates(self):
        """Шаблон index сформирован с правильным контекстом."""
        response = self.authorized_client.get(reverse('index'))
        form_fields = {
            'text': forms.fields.CharField,
            'pub_date': forms.fields.DateTimeField,
            'author': forms.fields.ChoiceField,
            'group': forms.fields.ChoiceField,
        }
        for value in form_fields.items():
            with self.subTest(value=value):
                self.assertIn('page', response.context)

    def test_context_homepage(self):
        """Словарь контекст выводит данные на страницу index"""
        response = self.guest_client.get(reverse('index'))
        first_object = response.context['page'][0]
        text_0 = first_object.text
        self.assertEqual(text_0, 'test-text')

    def test_context_group(self):
        """Словарь выводит данные на страницу group_post"""
        response = self.guest_client.get(reverse('group_posts',
                                                 kwargs={'slug': 'test-slug'}))
        first_object = response.context['group']
        title_0 = first_object.title
        slug_0 = first_object.slug
        description_0 = first_object.description
        self.assertEqual(title_0, 'test-title')
        self.assertEqual(slug_0, 'test-slug')
        self.assertEqual(description_0, 'test-description')

    def test_context_new_post(self):
        """Словарь выводит данные на страницу new_post"""
        response = self.authorized_client.get(reverse('new_post'))
        form_filed = {
            'text': forms.fields.CharField,
            'group': forms.fields.ChoiceField
        }
        for name, form in form_filed.items():
            with self.subTest(name=name):
                form_field = response.context['form'].fields[name]
                self.assertIsInstance(form_field, form)

    def test_context_post_edit(self):
        """Правильный контекст для post_edit"""
        response = self.authorized_client.get(reverse(
            'post_edit', kwargs={'username': 'mike', 'post_id': 1}))
        form_filed = {
            'text': forms.fields.CharField,
            'group': forms.fields.ChoiceField
        }
        for name, form in form_filed.items():
            with self.subTest(name=name):
                form_field = response.context['form'].fields[name]
                self.assertIsInstance(form_field, form)

    def test_context_profile(self):
        """Проверка контекста для profile"""
        response = self.guest_client.get(reverse(
            'profile', kwargs={'username': 'mike'}))
        first_object = response.context['page'][0]
        text_0 = first_object.text
        author_0 = first_object.author
        self.assertEqual(text_0, 'test-text')
        self.assertEqual(author_0, self.user)

    def test_context_break_post(self):
        """Проверка контекста для отдельного поста"""
        response = self.guest_client.get(reverse(
            'post', kwargs={'username': 'mike', 'post_id': 1}))
        first_object = response.context['post']
        text_0 = first_object.text
        author_0 = first_object.author
        self.assertEqual(text_0, 'test-text')
        self.assertEqual(author_0, self.user)


class PaginatorViewsTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        user = User.objects.create_user('Mike')
        cls.post = Post.objects.create(
            text='test1',
            author=user,
        )
        cls.post1 = Post.objects.create(
            text='test2',
            author=user,
        )
        cls.post1 = Post.objects.create(
            text='test3',
            author=user,
        )
        cls.post1 = Post.objects.create(
            text='test4',
            author=user,
        )
        cls.post1 = Post.objects.create(
            text='test5',
            author=user,
        )
        cls.post1 = Post.objects.create(
            text='test6',
            author=user,
        )
        cls.post1 = Post.objects.create(
            text='test7',
            author=user,
        )
        cls.post1 = Post.objects.create(
            text='test8',
            author=user,
        )
        cls.post1 = Post.objects.create(
            text='test9',
            author=user,
        )
        cls.post1 = Post.objects.create(
            text='test10',
            author=user,
        )
        cls.post1 = Post.objects.create(
            text='test11',
            author=user,
        )
        cls.post1 = Post.objects.create(
            text='test12',
            author=user,
        )
        cls.post1 = Post.objects.create(
            text='test13',
            author=user,
        )
        cls.post1 = Post.objects.create(
            text='test14',
            author=user,
        )

    def setUp(self):
        self.guest_client = Client()
        self.user = User.objects.create_user(username='Marcys')
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_paginator_homepage(self):
        """"Paginator выполняет свои действия"""
        response = self.authorized_client.get(reverse('index'))
        self.assertEqual(len(response.context['page'].object_list), 10)
