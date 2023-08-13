from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import View, ListView, DetailView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Task, Question
from .utils import parse_task_questions


'''
Сделать пермишны для неавторизованных
Добавить .env
Валидаторы на задание
Миксины
'''

menu = [
    {'title': 'Главная', 'url_name': 'home'},
    {'title': 'Мои задания', 'url_name': 'tasks'},
    {'title': 'Создать задание', 'url_name': 'createtask'}
]

# Create your views here.


def index(request):
    return render(request, template_name='tasks/index.html', context={'menu': menu, 'title': 'Главная'})


class CreateTask(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'tasks/create_task.html', context={'title': 'Создание задания', 'menu': menu})


class MyTasks(LoginRequiredMixin, ListView):
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


class ShowTask(LoginRequiredMixin, DetailView):
    model = Task
    template_name = 'tasks/show_task.html'
    context_object_name = 'task'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        questions = Question.objects.filter(task_id=self.kwargs['pk'])
        # questions = parse_task_questions(questions_query)

        c_def = {'title': kwargs['object'].title, 'menu': menu, 'questions': questions}
        return {**context, **c_def}


class DeleteTask(LoginRequiredMixin, DeleteView):
    model = Task
    template_name = 'tasks/delete_task.html'
    success_url = reverse_lazy('tasks')
    context_object_name = 'task'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = {'title': 'Удаление задания', 'menu': menu}
        return {**context, **c_def}

