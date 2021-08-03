from django.test.testcases import TestCase
from django.urls import reverse
from posts.models import Post, User

TEST_USERNAME = 'mike'
TEST_SLUG = 'test-slug'
POST_TEXT = 'Проверка создание поста'


class RoutesTest(TestCase):
    def test_url_routting(self):
        user = User.objects.create_user(TEST_USERNAME)
        post = Post.objects.create(
            text=POST_TEXT,
            author=user)
        route_names = {
            reverse('index'): '/',
            reverse('new_post'): '/new/',
            reverse('group_posts', kwargs={
                    'slug': TEST_SLUG}): f'/group/{TEST_SLUG}/',
            reverse('profile', kwargs={
                    'username': TEST_USERNAME}): f'/{TEST_USERNAME}/',
            reverse('post', kwargs={
                    'username': user.username,
                    'post_id': post.id}): f'/{TEST_USERNAME}/{post.id}/',
            reverse('post_edit', kwargs={
                    'username': user.username,
                    'post_id': post.id}): f'/{TEST_USERNAME}/{post.id}/edit/'
        }
        for name, url in route_names.items():
            self.assertEqual(name, url)
