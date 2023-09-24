from django import forms
from .models import Task


class SearchTaskForm(forms.Form):
    identifier = forms.CharField(label='Идентификатор', required=False)


class UploadFileForm(forms.Form):
    file = forms.FileField()
