from django.shortcuts import render
from django.views.generic import View, ListView

from .models import Task

# Create your views here.


class CreateTask(View):
    def get(self, request):
        return render(request, 'tasks/create_task.html')


class MyTasks(ListView):
    model = Task
    template_name = "tasks/tasks_view.html"
    context_object_name = 'tasks'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = {'title': 'Задания'}
        return {**context, **c_def}

    def get_queryset(self):
        new_queryset = Task.objects.filter(creator_id=self.request.user.id)
        return new_queryset
