from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

from .utils import generate_identifier

# Create your models here.


class Task(models.Model):
    title = models.CharField(verbose_name='Название', max_length=50)
    addition = models.FileField(verbose_name='Материалы', null=True)
    creator = models.ForeignKey(User, verbose_name='Создатель', on_delete=models.CASCADE)
    identifier = models.IntegerField(verbose_name='Идентификатор', default=generate_identifier)
    upload = models.FileField(upload_to="uploads/%Y/%m/%d/", null=True)
    slug = models.SlugField(verbose_name='URL', max_length=255, unique=True, db_index=True)
    feedback = models.BooleanField(verbose_name="Показывать результат", null=True)
    attempts = models.IntegerField(verbose_name="Количество попыток", default=0, null=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('task', kwargs={'slug': self.slug})

    class Meta:
        ordering = ('creator', 'title')
        verbose_name = 'Задание'
        verbose_name_plural = 'Задания'


class Question(models.Model):
    title = models.CharField(verbose_name='Название', max_length=255)
    test_type = models.BooleanField(verbose_name='Тестовый')
    variants = models.JSONField(verbose_name='Варианты', default=None, null=True)
    task = models.ForeignKey('Task', verbose_name='Задание', on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('task', 'title')
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'


class Answer(models.Model):
    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE)
    task = models.ForeignKey(Task, verbose_name='Задание', on_delete=models.CASCADE)
    content = models.JSONField(verbose_name='Ответ', default=None, null=True)

    def __str__(self):
        return f'{self.user.username}, {self.task.title}, {self.content}'

    class Meta:
        ordering = ('user', 'task')
        verbose_name = 'Ответ'
        verbose_name_plural = 'Ответы'
