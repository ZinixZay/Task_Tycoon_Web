from django.urls import path
from .views import CreateTask, MyTasks, Index, ShowTask, DeleteTask, SearchTask, \
    SolveTask, SolutionTaskShow, SolutionShow
from .viewsets import TaskAPIView, AnswerAPIView, QuestionAPIView

urlpatterns = [
    path('api/v1/tasks/', TaskAPIView.as_view(), name='apitasks'),
    path('api/v1/answers/', AnswerAPIView.as_view(), name='apianswers'),
    path('api/v1/questions/', QuestionAPIView.as_view(), name='apiquestions'),

    path('task_solve/<slug:slug>/', SolveTask.as_view(), name='solve'),
    path('task_solve/', SolveTask.as_view(), name='solve'),
    path('task_search/', SearchTask.as_view(), name='search'),
    path('solution/<int:pk>/', SolutionShow.as_view(), name='solution'),
    path('solutiontask/<slug:slug>/', SolutionTaskShow.as_view(), name='solution_task'),
    path('delete/<slug:slug>/', DeleteTask.as_view(), name='delete'),
    path('createtask/', CreateTask.as_view(), name='createtask'),
    path('tasks/', MyTasks.as_view(), name='tasks'),
    path('task/<slug:slug>/', ShowTask.as_view(), name='task'),
    path('', Index.as_view(), name='home')
]
