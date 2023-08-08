from django.shortcuts import render, redirect, HttpResponse
from django.views.generic import View, DetailView

from .models import Task

# Create your views here.


class CreateTask(View):
    def get(self, request):
        return render(request, 'tasks/create_task.html')

#
# class TaskView(DetailView):
#     model = Task
#
#     def get_context_data(self, **kwargs):
