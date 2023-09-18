from rest_framework.decorators import action
from rest_framework import viewsets
from rest_framework.response import Response

from .models import Task, Question, Answer
from .serializers import AnswerSerializer, TaskSerializer, QuestionSerializer
from .utils import generate_slug
from .permissions import IsAuthor


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def create(self, request, **kwargs):
        result = request.data
        title = result.pop('0')

        if len(Task.objects.filter(creator_id=request.user.id)) >= 3 or len(result.keys()) == 0:
            return Response({'status': 'Forbidden', 'error': 'maximum amount of tasks'})

        slug = generate_slug(title=title, task_model=Task)

        new_task = Task.objects.create(title=title, creator_id=request.user.id, slug=slug)

        for num in result.keys():
            question = result[num]
            if question['responses']:
                Question.objects.create(title=question['task_name'], test_type=True,
                                        variants=question['responses'], task=new_task)
            else:
                Question.objects.create(title=question['task_name'], test_type=False, task=new_task)
        return Response({'status': 'OK', 'identifier': new_task.identifier})


class AnswerViewSet(viewsets.ModelViewSet):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    permission_classes = (IsAuthor, )

    @action(methods=['get'], detail=True)
    def user(self, request, pk=None):
        result = Answer.objects.filter(user_id=pk).values()
        return Response({'answers': result})

    @action(methods=['get'], detail=True)
    def task(self, request, pk=None):
        result = Answer.objects.filter(task_id=pk).values()
        return Response({'answers': result})


class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

    @action(methods=['get'], detail=True)
    def task(self, request, pk=None):
        result = Question.objects.filter(task_id=pk).values()
        return Response({'questions': result})
