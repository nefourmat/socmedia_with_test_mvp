from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Group(models.Model):
    title = models.CharField(max_length=200,
                             verbose_name='Заголовок')
    slug = models.SlugField(max_length=150,
                            unique=True,
                            verbose_name='Ключ для создания адреса')
    description = models.TextField(blank=True,
                                   verbose_name='Описание')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Группы'
        verbose_name_plural = 'Группы'


class Post(models.Model):
    text = models.TextField(max_length=1000, verbose_name='Текст')
    pub_date = models.DateTimeField(auto_now_add=True,
                                    verbose_name='Дата публикации')
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='posts',
                               null=True,
                               verbose_name='Автор')
    group = models.ForeignKey(Group,
                              on_delete=models.SET_NULL,
                              related_name='posts',
                              blank=True,
                              null=True,
                              verbose_name='Группа')

    def __str__(self):
        return self.text[:15]

    class Meta:
        ordering = ['-pub_date']
        verbose_name = 'Посты'
        verbose_name_plural = 'Посты'
