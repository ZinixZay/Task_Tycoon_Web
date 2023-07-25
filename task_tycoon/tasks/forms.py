from django import forms
from tasks.models import Task


class AddTaskForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = Task
        fields = ['title', 'content']

