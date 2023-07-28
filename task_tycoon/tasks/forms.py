from django import forms
from tasks.models import Task


class AddTaskForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = Task
        fields = ['title', 'tests', 'questions']


class TaskStructureForm(forms.Form):
    title = forms.CharField(label='Название задания', max_length=50, required=True)
    tests = forms.IntegerField(label='Количество тестовых вопросов', required=True, initial=0)
    questions = forms.IntegerField(label='Количество вопросов с развернутым ответом', required=True, initial=0)

