from django.test.testcases import TestCase
from django.urls import reverse
from posts.models import Post, User

TEST_USERNAME = 'mike'
TEST_SLUG = 'test-slug'
POST_TEXT = 'Проверка создание поста'
GROUP = reverse('group_posts', kwargs={'slug': TEST_SLUG})


class RoutesTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(TEST_USERNAME)
        cls.post = Post.objects.create(
            text=POST_TEXT,
            author=cls.user)

    def test(self):
        route_names = [
            ['index', [], '/'],
            ['new_post', [], '/new/'],
            ['group_posts', [TEST_SLUG], f'/group/{TEST_SLUG}/'],
            ['profile', [TEST_USERNAME], f'/{TEST_USERNAME}/'],
            ['post', [TEST_USERNAME, self.post.id],
                f'/{TEST_USERNAME}/{self.post.id}/'],
            ['post_edit', [TEST_USERNAME, self.post.id],
                f'/{TEST_USERNAME}/{self.post.id}/edit/']
        ]
        for name, param, url in route_names:
            self.assertEqual(reverse(name, args=(param)), url)
