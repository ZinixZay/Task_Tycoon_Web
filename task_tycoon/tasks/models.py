from django.db import models
from django.contrib.auth.models import User
from .utils import generate_identifier

# Create your models here.


class Task(models.Model):
    title = models.CharField(verbose_name='Название', max_length=50)
    addition = models.FileField(verbose_name='Материалы', null=True)
    creator = models.ForeignKey(User, verbose_name='Создатель', on_delete=models.CASCADE)
    identifier = models.IntegerField(verbose_name='Идентификатор', default=generate_identifier)

    def __str__(self):
        return self.title


class Question(models.Model):
    title = models.CharField(verbose_name='Название', max_length=50)
    test_type = models.BooleanField(verbose_name='Тестовый')
    variants = models.JSONField(verbose_name='Варианты', default=None, null=True)
    task = models.ForeignKey('Task', verbose_name='Задание', on_delete=models.CASCADE)
