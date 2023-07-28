from django.shortcuts import render, redirect, HttpResponse
from django.views.generic import View

from .forms import AddTaskForm, TaskStructureForm
from .models import Task

# Create your views here.


class CreateTask(View):
    def post(self, request):
        form = TaskStructureForm(request.POST)
        if form.is_valid():
            return redirect('createtask', context=form.cleaned_data)


    def get(self, request):
        return render(request, 'tasks/task-structure.html', {'form': TaskStructureForm, 'title': 'Структура задания'})
