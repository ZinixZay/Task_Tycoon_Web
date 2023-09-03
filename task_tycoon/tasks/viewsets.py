from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Task, Question, Answer
from .serializers import TasksSerializer
from .utils import generate_slug


class TaskAPIView(APIView):
    def get(self, request):
        tasks = Task.objects.all().values()
        return Response({'tasks': list(tasks)})

    def post(self, request):
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


class AnswersAPIView(APIView):
    def get(self, request):
        answers = Answer.objects.all().values()
        return Response({'answers': list(answers)})


class QuestionAPIView(APIView):
    def get(self, request):
        question = Question.objects.all().values()
        return Response({'questions': list(question)})
