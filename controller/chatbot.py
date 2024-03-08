from use_case import question, ner


def question_controller():
    question.question("Hello")


def ner_controller():
    ner.ner("My name is Jhon")


ner_controller()