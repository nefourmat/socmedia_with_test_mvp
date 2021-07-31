from django.test import Client, TestCase
from django.urls import reverse

from posts.models import Group, Post, User
from posts.settings import PAGINATOR_COUNT

TEST_USERNAME = 'mike'
TEST_TEXT = 'test-text'
TEST_SLUG = 'test-slug'
TEST_TITLE = 'test-title'
TEST_TITLE_2 = 'test-another'
TEST_SLUG_2 = 'test-slug_2'
TEST_DESCRIPTION_2 = 'test-description_2'
TEST_DESCRIPTION = 'test-description'
HOMEPAGE_URL = reverse('index')
GROUP_POST_URL = reverse('group_posts', kwargs={'slug': TEST_SLUG})
PROFILE_URL = reverse('profile', kwargs={'username': TEST_USERNAME})
POST_URL = reverse('post', kwargs={'username': TEST_USERNAME, 'post_id': 1})


class ViewsTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(TEST_USERNAME)
        cls.gpoup = Group.objects.create(
            title=TEST_TITLE,
            slug=TEST_SLUG,
            description=TEST_DESCRIPTION)
        cls.another_group = Group.objects.create(
            title=TEST_TITLE_2,
            slug=TEST_SLUG_2,
            description=TEST_DESCRIPTION_2)
        cls.post = Post.objects.create(
            text=TEST_TEXT,
            group=cls.gpoup,
            author=cls.user)

    def setUp(self):
        """Создаем пользователя"""
        self.guest_client = Client()
        self.user = ViewsTests.user
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_context(self):
        """Проверка контекста"""
        urls = PROFILE_URL, GROUP_POST_URL, HOMEPAGE_URL
        for check_url in urls:
            response = self.guest_client.get(check_url)
            first_object = response.context['page'][0]
            text_0 = first_object.text
            if self.post.author == self.user:
                author_0 = first_object.author
            group_0 = first_object.group
            self.assertEqual(text_0, TEST_TEXT)
            self.assertEqual(author_0, self.user)
            self.assertEqual(group_0, self.post.group)

    def test_another_group(self):
        """Пост находиться в нужной группе"""
        self.assertNotIn(self.post, self.another_group.posts.all())


class PaginatorViewsTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(TEST_USERNAME)
        for i in range(1, 11):
            cls.post = Post.objects.create(
                text=TEST_TEXT,
                author=cls.user)

    def setUp(self):
        self.guest_client = Client()
        self.user = PaginatorViewsTest.user
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_paginator_homepage(self):
        """"Paginator выполняет свои действия"""
        response = self.authorized_client.get(HOMEPAGE_URL)
        self.assertEqual(len(
            response.context['page'].object_list), PAGINATOR_COUNT)
