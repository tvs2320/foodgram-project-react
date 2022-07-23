from django.contrib.auth.models import AbstractUser
from django.db import models

from .validators import username_validate


class CustomUser(AbstractUser):
    email = models.EmailField(max_length=254,
                              unique=True,
                              verbose_name='Адрес электронной почты')
    username = models.CharField(max_length=150,
                                unique=True,
                                validators=[username_validate],
                                verbose_name='Имя пользователя')
    first_name = models.CharField(max_length=150,
                                  verbose_name='Имя')
    last_name = models.CharField(max_length=150,
                                 verbose_name='Фамилия')
    password = models.CharField(max_length=150,
                                verbose_name='Пароль')

    # USERNAME_FIELD = 'email'
    # REQUIRED_FIELDS = ['username']

    class Meta:
        ordering = ('username',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username


class Follow(models.Model):
    follower = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Подписчик',
    )
    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Автор'
    )

    def __str__(self):
        return f"Подписчик: '{self.follower}', Автор: '{self.author}'"

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['follower', 'author'],
                name='stop_self_follow'
            )
        ]
