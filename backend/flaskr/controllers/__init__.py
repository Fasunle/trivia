from flask import Blueprint
from random import randint

categories_controller = Blueprint("categories", __name__)
question_controller = Blueprint("questions", __name__)


def get_random_integer(length=0):
    return randint(0, length - 1)
