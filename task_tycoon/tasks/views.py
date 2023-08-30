from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import View, ListView, DetailView, DeleteView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Task, Question, Answer
from .forms import SearchTaskForm
from .utils import parse_answer_to_dict, check_solution_exists, analyse_answer, \
    DataMixin, AuthorRequiredMixin



'''
Админка
Добавить .env
Задай вопрос, почему не могу импортировать модель в utils
'''


# Create your views here.


class Index(DataMixin, View):
    def get(self, request):
        if self.request.user.is_authenticated:
            return render(self.request, template_name='tasks/index.html', context=self.set_context(title='Главная'))
        else:
            return redirect('registration')


class SolutionShow(DataMixin, LoginRequiredMixin, DetailView):
    model = Answer
    template_name = 'tasks/show_solution.html'
    context_object_name = 'answer'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.set_context(title=f'Ответы на "{kwargs["object"].task}"')
        question_query = Question.objects.filter(task=kwargs["object"].task)
        user_solution = Answer.objects.get(task=kwargs["object"].task, user=self.request.user)
        answer_result = analyse_answer(question_query, user_solution)
        return {**context, **c_def, 'result': answer_result}


class SolutionTaskShow(DataMixin, AuthorRequiredMixin, ListView):
    model = Answer
    template_name = 'tasks/show_solutions.html'
    context_object_name = 'answers'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        task_title = Task.objects.get(pk=self.kwargs['pk']).title
        c_def = self.set_context(title=f'Ответы на "{task_title}"')
        return {**context, **c_def}

    def get_queryset(self):
        queryset = Answer.objects.filter(task=self.kwargs['pk'])
        return queryset

    def get_object(self):
        return Task.objects.get(pk=self.kwargs['pk'])


class AnswerTask(DataMixin, AuthorRequiredMixin, DetailView):
    login_url = 'answer'
    model = Task
    template_name = 'tasks/task_answer.html'
    context_object_name = 'task'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        questions = Question.objects.filter(task_id=self.kwargs['pk'])

        c_def = self.set_context(title=kwargs['object'].title, questions=questions)
        return {**context, **c_def}


class SearchTask(DataMixin, LoginRequiredMixin, TemplateView):
    template_name = 'tasks/task_search.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.set_context(title='Поиск', form=SearchTaskForm(self.request.GET))
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


class SolveTask(DataMixin, LoginRequiredMixin, TemplateView):
    template_name = 'tasks/solve_task.html'

    def get_context_data(self, **kwargs):
        task = Task.objects.filter(identifier=kwargs['identifier'])[0]
        questions = Question.objects.filter(task_id=task.id)
        context = super().get_context_data(**kwargs)
        c_def = self.set_context(title=f'Решение {task.title}', questions=questions, task=task)
        return {**context, **c_def}

    def post(self, *args):
        answer = parse_answer_to_dict(self.request.POST)
        task = Task.objects.get(title=answer.pop('task_title'))
        if check_solution_exists(Answer, task, self.request.user):
            return redirect('home')
        Answer.objects.create(user=self.request.user, task=task, content=answer)
        return redirect('home')


class CreateTask(DataMixin, LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'tasks/create_task.html', context=self.set_context(title='Создание задания'))


class MyTasks(DataMixin, LoginRequiredMixin, ListView):
    model = Task
    template_name = "tasks/tasks_view.html"
    context_object_name = 'tasks'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.set_context(title='Задания')
        return {**context, **c_def}

    def get_queryset(self):
        new_queryset = Task.objects.filter(creator_id=self.request.user.id)
        if new_queryset:
            return reversed(new_queryset)
        return []


class ShowTask(DataMixin, AuthorRequiredMixin, DetailView):
    model = Task
    template_name = 'tasks/show_task.html'
    context_object_name = 'task'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        questions = Question.objects.filter(task_id=self.kwargs['pk'])

        c_def = self.set_context(title=kwargs['object'].title, questions=questions)
        return {**context, **c_def}


class DeleteTask(DataMixin, AuthorRequiredMixin, DeleteView):
    model = Task
    template_name = 'tasks/delete_task.html'
    success_url = reverse_lazy('tasks')
    context_object_name = 'task'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.set_context(title='Удаление задания')
        return {**context, **c_def}
