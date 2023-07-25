from django.urls import path
from .views import AddTask

urlpatterns = [
    path('tasks/', AddTask.as_view())
]
