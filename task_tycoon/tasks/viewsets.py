from rest_framework.decorators import action
from rest_framework import viewsets
from rest_framework.response import Response

from .models import Task, Question, Answer
from .serializers import AnswerSerializer, TaskSerializer, QuestionSerializer
from .utils import generate_slug
from .permissions import IsAuthor


class TaskViewSet(viewsets.ModelViewSet):
    """
    General Task ViewSet class
    """
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def create(self, request, **kwargs):
        """
        Parses info from request, checks permission and create object
        :param request:
        :param kwargs:
        :return: if no permission - response with status forbidden
        else creates task and questions connected
        """
        result = request.data
        print(result)
        title = result.pop('0')

        if len(Task.objects.filter(creator_id=request.user.id)) >= 3 or len(result.keys()) == 0:
            return Response({'status': 'Forbidden', 'error': 'maximum amount of tasks'})

        slug = generate_slug(title=title, task_model=Task)

        new_task = Task.objects.create(title=title, creator_id=request.user.id, slug=slug)

        for num in result.keys():
            question = result[num]
            if 'responses' in question.keys():
                Question.objects.create(title=question['task_name'], test_type=True,
                                        variants=question['responses'], task=new_task)
            else:
                Question.objects.create(title=question['task_name'], test_type=False,
                                        task=new_task, variants=question["response_textarea"][0])
        return Response({'status': 'OK', 'identifier': new_task.identifier})


class AnswerViewSet(viewsets.ModelViewSet):
    """
    General Answer ViewSet class
    """
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    permission_classes = (IsAuthor, )

    @action(methods=['get'], detail=True)
    def user(self, request, pk=None):
        """
        Returns answers created by one user
        :param request:
        :param pk: if user pk exists takes it
        :return: returns answers, given by one user with same pk
        """
        result = Answer.objects.filter(user_id=pk).values()
        return Response({'answers': result})

    @action(methods=['get'], detail=True)
    def task(self, request, pk=None):
        """
        Return answer for only 1 task
        :param request:
        :param pk: if task pk exists takes it
        :return: all answers for 1 task
        """
        result = Answer.objects.filter(task_id=pk).values()
        return Response({'answers': result})


class QuestionViewSet(viewsets.ModelViewSet):
    """
    General Question ViewSet class
    """
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

    @action(methods=['get'], detail=True)
    def task(self, request, pk=None):
        """
        Return all questions for 1 task
        :param request:
        :param pk: if pk exists takes it
        :return: all tasks for 1 task
        """
        result = Question.objects.filter(task_id=pk).values()
        return Response({'questions': result})
