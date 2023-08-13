from django.urls import path
from .views import CreateTask, MyTasks, index, ShowTask
from .viewsets import TaskAPIView

urlpatterns = [
    path('createtask/', CreateTask.as_view(), name='createtask'),
    path('api/v1/addtask', TaskAPIView.as_view(), name='addtask'),
    path('tasks/', MyTasks.as_view(), name='tasks'),
    path('task/<int:pk>/', ShowTask.as_view(), name='task'),
    path('', index, name='home')
]
