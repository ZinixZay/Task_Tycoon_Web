from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response

from .models import Task, Question, Answer
from .serializers import TasksSerializer


class ShowTasksAPIView(ListAPIView):
    queryset = Task.objects.all()
    serializer_class = TasksSerializer


class CreateTaskAPIView(APIView):
    """
    API, creates task on post request, validating null from
    """
    def post(self, request):
        result = request.data
        title = result.pop('0')

        if len(Task.objects.filter(creator_id=request.user.id)) >= 3 or len(result.keys()) == 0:
            return Response({'status': 'Forbidden', 'error': 'maximum amount of tasks'})

        new_task = Task.objects.create(title=title, creator_id=request.user.id)

        for num in result.keys():
            question = result[num]
            if question['responses']:
                Question.objects.create(title=question['task_name'], test_type=True,
                                        variants=question['responses'], task=new_task)
            else:
                Question.objects.create(title=question['task_name'], test_type=False, task=new_task)
        return Response({'status': 'OK', 'identifier': new_task.identifier})
