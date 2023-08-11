from django.urls import path
from .views import CreateTask, MyTasks, index
from .viewsets import TaskAPIView

urlpatterns = [
    path('createtask/', CreateTask.as_view(), name='createtask'),
    path('api/v1/addtask', TaskAPIView.as_view(), name='addtask'),
    path('tasks/', MyTasks.as_view(), name='tasks'),
    path('', index, name='home')
]
