from django.shortcuts import render
from django.views.generic import View, ListView, DetailView

from .models import Task


menu = [
    {'title': 'Главная', 'url_name': 'home'},
    {'title': 'Мои задания', 'url_name': 'tasks'},
    {'title': 'Создать задание', 'url_name': 'createtask'}
]

# Create your views here.


def index(request):
    return render(request, template_name='tasks/index.html', context={'menu': menu, 'title': 'Главная'})


class CreateTask(View):
    def get(self, request):
        return render(request, 'tasks/create_task.html', context={'title': 'Создание задания', 'menu': menu})


class MyTasks(ListView):
    model = Task
    template_name = "tasks/tasks_view.html"
    context_object_name = 'tasks'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = {'title': 'Задания', 'menu': menu}
        return {**context, **c_def}

    def get_queryset(self):
        new_queryset = Task.objects.filter(creator_id=self.request.user.id)
        return new_queryset


class ShowTask(DetailView):
    template_name = 'tasks/show_task.html'

