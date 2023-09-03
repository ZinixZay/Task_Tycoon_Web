from rest_framework import serializers
from .models import Task, Question, Answer


class TasksSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ('title', 'identifier', 'addition', 'creator', 'slug')
