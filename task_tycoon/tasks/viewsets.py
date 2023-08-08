from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Task


class TaskAPIView(APIView):
    def post(self, request):
        result = request.data
        title = result.pop('0')
        new_task = Task.objects.create(title=title, creator_id=request.user.id, content=result)
        return Response({'status': 'OK', 'identifier': new_task.identifier})
