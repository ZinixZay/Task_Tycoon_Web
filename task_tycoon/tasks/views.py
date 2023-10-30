import os

from django.http import FileResponse, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import View, ListView, DetailView, DeleteView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django_sendfile import sendfile

from .models import Task, Question, Answer
from .forms import SearchTaskForm, UploadFileForm, SetupTaskForm
from .utils import parse_answer_to_dict, check_solution_allowed, analyse_answer, \
    DataMixin, AuthorRequiredMixin, generate_excel


# Create your views here.


class SolutionShow(DataMixin, LoginRequiredMixin, DetailView):
    """
    Detail View of user's solution. Answer analyse function comes from utils.
    """
    model = Answer
    template_name = 'tasks/show_solution.html'
    context_object_name = 'answer'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.set_context(title=f'Ответы на "{kwargs["object"].task}"')
        question_query = Question.objects.filter(task=kwargs["object"].task)
        user_solution = kwargs["object"]
        answer_result = analyse_answer(question_query, user_solution)
        return {**context, **c_def, 'result': answer_result}


class SolutionTaskShow(DataMixin, AuthorRequiredMixin, ListView):
    """
    Shows all answers for task
    """
    model = Answer
    template_name = 'tasks/show_solutions.html'
    context_object_name = 'answers'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        task_title = Task.objects.get(slug=self.kwargs['slug']).title
        c_def = self.set_context(title=f'Ответы на "{task_title}"', slug=self.kwargs['slug'])
        return {**context, **c_def}

    def get_queryset(self):
        queryset = Answer.objects.filter(task=Task.objects.get(slug=self.kwargs['slug']))
        return queryset

    def get_object(self):
        return Task.objects.get(slug=self.kwargs['slug'])


class SearchTask(DataMixin, LoginRequiredMixin, TemplateView):
    """
    Shows page where user can find task by identifier
    """
    template_name = 'tasks/task_search.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.set_context(title='Поиск', form=SearchTaskForm(self.request.GET))
        return {**context, **c_def}

    def post(self, *args):
        form = SearchTaskForm(self.request.POST)
        if form.is_valid():
            identifier = form.cleaned_data['identifier']
            task = Task.objects.filter(identifier=identifier)
            if task:
                return redirect('solve', slug=task[0].slug)
            else:
                return redirect('search')


class SolveTask(DataMixin, LoginRequiredMixin, TemplateView):
    """
    Shows page with all questions for one task, where user can solve them
    """
    template_name = 'tasks/solve_task.html'

    def get_context_data(self, **kwargs):
        task = Task.objects.filter(slug=kwargs['slug'])[0]
        questions = Question.objects.filter(task_id=task.id)
        context = super().get_context_data(**kwargs)
        c_def = self.set_context(title=f'Решение {task.title}', questions=questions, task=task)
        return {**context, **c_def}

    def post(self, *args):
        answer = parse_answer_to_dict(self.request.POST)
        task = Task.objects.get(title=answer.pop('task_title'))
        if check_solution_allowed(Answer, task, self.request.user):
            result = Answer.objects.create(user=self.request.user, task=task, content=answer)
            if task.feedback:
                return redirect('solution', result.pk)
            else:
                return redirect('search')
        return redirect('home')


class CreateTask(DataMixin, LoginRequiredMixin, View):
    """
    Renders page with task creation
    """
    def get(self, request):
        return render(request, 'tasks/create_task.html', context=self.set_context(title='Создание задания'))


class MyTasks(DataMixin, LoginRequiredMixin, ListView):
    """
    Page with all user created tasks
    """
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
    """
    Shows task content with right and false variants in test questions or non-test questions type
    """
    model = Task
    template_name = 'tasks/show_task.html'
    context_object_name = 'task'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        questions = Question.objects.filter(task=Task.objects.get(slug=self.kwargs['slug']))

        c_def = self.set_context(title=kwargs['object'].title, questions=questions)
        return {**context, **c_def}


class DeleteTask(DataMixin, AuthorRequiredMixin, DeleteView):
    """
    Confirmation of deleting
    """
    model = Task
    template_name = 'tasks/delete_task.html'
    context_object_name = 'task'
    slug_field = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.set_context(title='Удаление задания')
        return {**context, **c_def}

    def get_success_url(self):
        return reverse_lazy('tasks')

    def form_valid(self, *args, **kwargs):
        task = self.get_object()
        if task.upload:
            os.remove(task.upload.path)
        task.delete()
        return redirect('tasks')


def download_file(request, slug):
    """
    Downloading connected file with task
    :param request:
    :param slug: slug of a task
    :return: file, connected with task
    """
    task = Task.objects.get(slug=slug)
    return FileResponse(task.upload, as_attachment=True)


def download_excel(request, slug):
    task = Task.objects.get(slug=slug)
    answers = Answer.objects.filter(task=task)
    questions = Question.objects.filter(task=task)
    excel_file_path = generate_excel(task, answers, questions)
    return sendfile(request, excel_file_path, attachment=True)


class UploadFile(DataMixin, View, AuthorRequiredMixin):
    """
    Uploading file to a server and connects it with a task
    """
    def post(self, request, slug):
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            if file.size > 50000000:
                return redirect('home')
            else:
                task = Task.objects.get(slug=slug)
                if task.upload:
                    os.remove(task.upload.path)
            task = Task.objects.get(slug=slug)
            task.upload = file
            task.save()
            return redirect('home')
        else:
            return reverse_lazy('tasks')

    def get(self, request, slug):
        return render(self.request, template_name='tasks/upload.html',
                      context=self.set_context(title='Загрузка файла', form=UploadFileForm, slug=slug))


class Index(DataMixin, View):
    """
    Rendering main page
    """
    def get(self, request):
        if self.request.user.is_authenticated:
            return render(self.request, template_name='tasks/index.html', context=self.set_context(title='Главная'))
        else:
            return redirect('registration')


class TaskSetup(DataMixin, View):
    """
    Rendering task setup page
    """
    def get(self, request, slug):
        task = Task.objects.get(slug=slug)
        form = SetupTaskForm
        return render(request, template_name="tasks/setup.html",
                      context=self.set_context(title="Настройка",
                                               task=task,
                                               form=form))

    def post(self, request, slug):
        form = SetupTaskForm(request.POST)
        if form.is_valid():
            task = Task.objects.get(slug=slug)
            task.feedback = form.cleaned_data['feedback']
            task.attempts = form.cleaned_data['attempts']
            task.save()
            return redirect('tasks')
