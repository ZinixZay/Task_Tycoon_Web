from random import randint
import json


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
