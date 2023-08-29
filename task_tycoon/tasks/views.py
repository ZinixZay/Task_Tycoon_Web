from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import View, ListView, DetailView, DeleteView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Task, Question, Answer
from .forms import SearchTaskForm
from .utils import parse_answer_to_dict, check_solution_exists, analyse_answer


'''
Админка
Сделать пермишны для неавторизованных (и чужих страниц)
Добавить .env
Валидаторы на задание
Миксины
Задай вопрос, почему не могу импортировать модель в utils
'''

menu = [
    {'title': 'Главная', 'url_name': 'home'},
    {'title': 'Мои задания', 'url_name': 'tasks'},
    {'title': 'Создать задание', 'url_name': 'createtask'},
    {'title': 'Решить задание', 'url_name': 'search'}
]

# Create your views here.


def index(request):
    return render(request, template_name='tasks/index.html', context={'menu': menu, 'title': 'Главная'})


class SolutionShow(LoginRequiredMixin, DetailView):
    model = Answer
    template_name = 'tasks/show_solution.html'
    context_object_name = 'answer'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = {'title': f'Ответы на "{kwargs["object"].task}"', 'menu': menu}
        question_query = Question.objects.filter(task=kwargs["object"].task)
        user_solution = Answer.objects.get(task=kwargs["object"].task, user=self.request.user)
        answer_result = analyse_answer(question_query, user_solution)
        return {**context, **c_def}


class SolutionTaskShow(LoginRequiredMixin, ListView):
    model = Answer
    template_name = 'tasks/show_solutions.html'
    context_object_name = 'answers'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        task_title = Task.objects.get(pk=self.kwargs['pk']).title
        c_def = {'title': f'Ответы на "{task_title}"', 'menu': menu}
        return {**context, **c_def}

    def get_queryset(self):
        queryset = Answer.objects.filter(task=self.kwargs['pk'])
        return queryset


class AnswerTask(LoginRequiredMixin, DetailView):
    model = Task
    template_name = 'tasks/task_answer.html'
    context_object_name = 'task'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        questions = Question.objects.filter(task_id=self.kwargs['pk'])

        c_def = {'title': kwargs['object'].title, 'menu': menu, 'questions': questions}
        return {**context, **c_def}


class SearchTask(LoginRequiredMixin, TemplateView):
    template_name = 'tasks/task_search.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = {'title': 'Поиск', 'menu': menu, 'form': SearchTaskForm(self.request.GET)}
        return {**context, **c_def}

    def post(self, *args):
        form = SearchTaskForm(self.request.POST)
        if form.is_valid():
            identifier = form.cleaned_data['identifier']
            task = Task.objects.filter(identifier=identifier)[0]
            if task:
                return redirect('solve', identifier=identifier)
            else:
                return redirect('search')


class SolveTask(LoginRequiredMixin, TemplateView):
    template_name = 'tasks/solve_task.html'

    def get_context_data(self, **kwargs):
        task = Task.objects.filter(identifier=kwargs['identifier'])[0]
        questions = Question.objects.filter(task_id=task.id)
        context = super().get_context_data(**kwargs)
        c_def = {'title': f'Решение {task.title}', 'menu': menu, 'questions': questions, 'task': task}
        return {**context, **c_def}

    def post(self, *args):
        answer = parse_answer_to_dict(self.request.POST)
        task = Task.objects.get(title=answer.pop('task_title'))
        if check_solution_exists(Answer, task, self.request.user):
            return redirect('home')
        Answer.objects.create(user=self.request.user, task=task, content=answer)
        return redirect('home')


class CreateTask(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'tasks/create_task.html', context={'title': 'Создание задания', 'menu': menu})


class MySolves(LoginRequiredMixin, ListView):
    pass


class MyTasks(LoginRequiredMixin, ListView):
    model = Task
    template_name = "tasks/tasks_view.html"
    context_object_name = 'tasks'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = {'title': 'Задания', 'menu': menu}
        return {**context, **c_def}

    def get_queryset(self):
        new_queryset = reversed(Task.objects.filter(creator_id=self.request.user.id))
        return new_queryset


class ShowTask(LoginRequiredMixin, DetailView):
    model = Task
    template_name = 'tasks/show_task.html'
    context_object_name = 'task'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        questions = Question.objects.filter(task_id=self.kwargs['pk'])

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

