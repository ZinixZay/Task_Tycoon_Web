from django.urls import path
from .views import CreateTask
from .viewsets import TaskAPIView

urlpatterns = [
    path('createtask/', CreateTask.as_view(), name='createtask'),
    path('api/v1/addtask', TaskAPIView.as_view(), name='addtask'),
]
