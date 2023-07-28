from django.db import models
from django.contrib.auth.models import User
from .utils import generate_identifier

# Create your models here.


class Task(models.Model):
    title = models.CharField(verbose_name='Название', max_length=50)
    content = models.JSONField(verbose_name='Задание')
    tests = models.IntegerField(verbose_name='Количество тестовых вопросов', )
    questions = models.IntegerField(verbose_name='Количество вопросов с развернутым ответом')
    creator = models.ForeignKey(User, verbose_name='Создатель', on_delete=models.CASCADE)
    identifier = models.IntegerField(verbose_name='Идентификатор', default=generate_identifier)

    def __str__(self):
        return self.title
