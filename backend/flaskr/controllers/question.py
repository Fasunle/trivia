from flask import (
    request,
    jsonify
)

from config import (
    QUESTIONS_PER_PAGE,
    ERROR_OUT,
    MAX_QUESTIONS_PER_PAGE
)
from flaskr.controllers import question_controller
from models import (
    Category,
    Question
)


@question_controller.route('/')
def fetch_questions():
    """Fetch Questions from the database and automatically paginate them.

    return 10 questions per page

    Returns:
        object : jsonify dictionary of format 

        {
        "questions": formatted_questions,
        "current_category": 2,
        "categories": format_categories,
        "total_questions": questions.total
    }
    """

    pass
