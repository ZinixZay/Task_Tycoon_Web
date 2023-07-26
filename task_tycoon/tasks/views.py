from django.shortcuts import render, redirect
from django.views.generic import View

from .forms import AddTaskForm, TaskStructureForm
from .models import Task

# Create your views here.


class MakeTaskStructure(View):
    def post(self, request):
        form = TaskStructureForm(request.POST)
        if form.is_valid():
            try:
                Task.objects.create(**form.cleaned_data)
                return redirect('createtask', context=form.cleaned_data)
            except Exception:
                form.add_error(None, 'Ошибка')

    def get(self, request):
        return render(request, 'tasks/task-structure.html', {'form': TaskStructureForm, 'title': 'Структура задания'})


class CreateTask(View):
    def get(self, request, context):
        print(**context)

