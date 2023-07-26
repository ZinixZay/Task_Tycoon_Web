from django.urls import path
from .views import MakeTaskStructure, CreateTask

urlpatterns = [
    path('taskstructure/', MakeTaskStructure.as_view(), name='taskstructure'),
    path('createtask/', CreateTask.as_view(), name='createtask')
]
