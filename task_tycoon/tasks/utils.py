from random import randint
import json
from django.contrib.auth.mixins import AccessMixin
from django.shortcuts import redirect

# Variables

menu = [
    {'title': 'Главная', 'url_name': 'home'},
    {'title': 'Мои задания', 'url_name': 'tasks'},
    {'title': 'Создать задание', 'url_name': 'createtask'},
    {'title': 'Решить задание', 'url_name': 'search'}
]


# Mixins


class DataMixin:

    def set_context(self, **kwargs):
        context = kwargs
        context['menu'] = menu
        return context


class AuthorRequiredMixin(AccessMixin):

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        if request.user != self.get_object().creator or request.user.is_staff:
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)


class TaskAuthorRequiredMixin(AccessMixin):

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        if request.user != self.get_object().task.creator or request.user.is_staff:
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)


# Functions


def generate_identifier():
    return randint(100000, 999999)


def parse_answer_to_dict(response) -> dict:
    str_response = str(response)
    str_response = str_response.replace("'", '"')
    dict_response = json.loads(str_response[12:len(str_response) - 1])
    content = {}
    task_title = None
    for header in dict_response:
        if header == 'csrfmiddlewaretoken':
            continue
        if header == 'task_title':
            task_title = dict_response[header]
            continue
        content[header] = dict_response[header]
    return {'task_title': task_title[0], **content}


def check_solution_exists(Answer, task, user) -> bool:
    solution = Answer.objects.filter(task=task, user=user)
    if solution:
        return True
    return False


def analyse_answer(question_query, user_answers) -> dict:
    # question_query parse

    right_answers = {}
    for question in question_query:
        if question.variants:
            right_answers[question.title] = [i['response_name'] for i in list(
                filter(lambda x: x['response_right'], question.variants))]

    result = {}
    for question, answer in user_answers.content.items():
        if question in right_answers.keys():
            if answer != right_answers[question]:
                result[question] = False
            else:
                result[question] = True
        else:
            result[question] = answer[0]
    return result
