from django.urls import path, include
from .views import CreateTask, MyTasks, Index, ShowTask, DeleteTask, SearchTask, \
    SolveTask, SolutionTaskShow, SolutionShow, UploadFile, download_file, download_excel, TaskSetup
from rest_framework import routers
from .viewsets import TaskViewSet, AnswerViewSet, QuestionViewSet

router_tasks = routers.DefaultRouter()
router_answers = routers.DefaultRouter()
router_questions = routers.DefaultRouter()

router_tasks.register(r'tasks', TaskViewSet, basename='apitasks')
router_answers.register(r'answers', AnswerViewSet, basename='apianswers')
router_questions.register(r'questions', QuestionViewSet, basename='apiquestions')

urlpatterns = [
    path('api/v1/', include(router_tasks.urls)),
    path('api/v1/', include(router_answers.urls)),
    path('api/v1/', include(router_questions.urls)),

    path('download/<slug:slug>/', download_file, name='download'),
    path('upload/<slug:slug>/', UploadFile.as_view(), name='upload'),
    path('task_solve/<slug:slug>/', SolveTask.as_view(), name='solve'),
    path('task_solve/', SolveTask.as_view(), name='solve'),
    path('task_search/', SearchTask.as_view(), name='search'),
    path('solution/<int:pk>/', SolutionShow.as_view(), name='solution'),
    path('solutiontask/<slug:slug>/', SolutionTaskShow.as_view(), name='solution_task'),
    path('delete/<slug:slug>/', DeleteTask.as_view(), name='delete'),
    path('createtask/', CreateTask.as_view(), name='createtask'),
    path('tasks/', MyTasks.as_view(), name='tasks'),
    path('task/<slug:slug>/', ShowTask.as_view(), name='task'),
    path('excel/<slug:slug>/', download_excel, name='excel_download'),
    path('settings/<slug:slug>/', TaskSetup.as_view(), name='setup'),
    path('', Index.as_view(), name='home')
]
