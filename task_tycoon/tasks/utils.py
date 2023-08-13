from random import randint

# Functions


def generate_identifier():
    return randint(100000, 999999)


def parse_task_questions(questions_query_set: list) -> list:
    questions = list()
    for question in questions_query_set:
        if question.variants:
            for response in question.variants:
                pass
    return []

