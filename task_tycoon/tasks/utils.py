from random import randint
import json
from transliterate import translit

from django.contrib.auth.mixins import AccessMixin
from django.utils.text import slugify

# Variables

menu = [
    {'title': 'Главная', 'url_name': 'home'},
    {'title': 'Мои задания', 'url_name': 'tasks'},
    {'title': 'Создать задание', 'url_name': 'createtask'},
    {'title': 'Решить задание', 'url_name': 'search'}
]

identifiers = list()

# Mixins


class DataMixin:
    """
    Collecting args and adding menu to a page
    """
    def set_context(self, **kwargs):
        context = kwargs
        context['menu'] = menu
        return context


class AuthorRequiredMixin(AccessMixin):
    """
    Permission mixin only for object author
    """
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        if request.user != self.get_object().creator:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)


# Functions


def generate_slug(title: str, task_model) -> str:
    """
    Generating slug for new task
    :param title: task's title
    :param task_model: Task model
    :return: generated slug
    """
    slug = slugify(title, allow_unicode=True)
    slug = translit(slug, 'ru', reversed=True)
    similar_slugs = sorted([i.slug for i in task_model.objects.all() if slug in i.slug])
    match len(similar_slugs):
        case 0:
            return slug
        case 1:
            return slug + '1'
    slug = similar_slugs[-1]
    return slug[:len(slug) - 1] + (str(int(slug[-1]) + 1))


def generate_identifier() -> int:
    """
    Generating random identifier for task. Checks if it is unique
    :return: identifier
    """
    from .models import Task
    while True:
        identifier = randint(100000, 999999)
        if identifier not in [i.identifier for i in Task.objects.all()]:
            break
    identifiers.append(identifier)
    return identifier


def parse_answer_to_dict(response) -> dict:
    """
    Parsing user's answer to a python dict
    :param response: user's task answer
    :return: parsed user's answer
    """
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
    """
    Check if user already answered this task. if yes -> does not accept this solution
    :param Answer: Answer model
    :param task: solution task
    :param user: solution user
    :return: True, if solution exists
    """
    solution = Answer.objects.filter(task=task, user=user)
    if solution:
        return True
    return False


def analyse_answer(question_query, user_answers) -> dict:
    """
    Gets user's solution, right solution from data and compare them. Forming a dict with right and false answers
    :param question_query: All in-task questions
    :param user_answers: User's solution
    :return: python dict with rightness of answers
    """
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
