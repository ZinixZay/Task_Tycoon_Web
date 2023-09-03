from rest_framework import serializers
from .models import Task, Question, Answer


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ('user_id', 'task_id', 'content')
