from django import forms
from tasks.models import Task


class SearchTaskForm(forms.Form):
    identifier = forms.CharField(label='Идентификатор', required=False)
