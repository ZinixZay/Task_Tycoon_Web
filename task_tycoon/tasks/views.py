from django.shortcuts import render, HttpResponse
from .forms import AddTaskForm
from django.views.generic import CreateView

# Create your views here.


class AddTask(CreateView):
    form_class = AddTaskForm
    template_name = 'tasks/base.html'

