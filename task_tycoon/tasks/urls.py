from django.urls import path
from .views import CreateTask, MyTasks, Index, ShowTask, DeleteTask, AnswerTask, SearchTask, \
    SolveTask, SolutionTaskShow, SolutionShow
from .viewsets import TaskAPIView

urlpatterns = [
    path('task_solve/<int:identifier>/', SolveTask.as_view(), name='solve'),
    path('task_solve/', SolveTask.as_view(), name='solve'),
    path('task_search/', SearchTask.as_view(), name='search'),
    path('answer/<int:pk>/', AnswerTask.as_view(), name='answer'),
    path('solution/<int:pk>/', SolutionShow.as_view(), name='solution'),
    path('solutiontask/<int:pk>/', SolutionTaskShow.as_view(), name='solution_task'),
    path('delete/<int:pk>/', DeleteTask.as_view(), name='delete'),
    path('createtask/', CreateTask.as_view(), name='createtask'),
    path('api/v1/addtask', TaskAPIView.as_view(), name='addtask'),
    path('tasks/', MyTasks.as_view(), name='tasks'),
    path('task/<int:pk>/', ShowTask.as_view(), name='task'),
    path('', Index.as_view(), name='home')
]
