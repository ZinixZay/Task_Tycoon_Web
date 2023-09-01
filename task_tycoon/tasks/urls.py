from django.urls import path
from .views import CreateTask, MyTasks, Index, ShowTask, DeleteTask, SearchTask, \
    SolveTask, SolutionTaskShow, SolutionShow
from .viewsets import CreateTaskAPIView, ShowTasksAPIView

urlpatterns = [
    path('api/v1/addtask', CreateTaskAPIView.as_view(), name='addtask'),
    path('api/v1/tasks', ShowTasksAPIView.as_view(), name='showtasks'),

    path('task_solve/<int:identifier>/', SolveTask.as_view(), name='solve'),
    path('task_solve/', SolveTask.as_view(), name='solve'),
    path('task_search/', SearchTask.as_view(), name='search'),
    path('solution/<int:pk>/', SolutionShow.as_view(), name='solution'),
    path('solutiontask/<int:pk>/', SolutionTaskShow.as_view(), name='solution_task'),
    path('delete/<int:pk>/', DeleteTask.as_view(), name='delete'),
    path('createtask/', CreateTask.as_view(), name='createtask'),
    path('tasks/', MyTasks.as_view(), name='tasks'),
    path('task/<int:pk>/', ShowTask.as_view(), name='task'),
    path('', Index.as_view(), name='home')
]
