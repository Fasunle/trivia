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
    # get page number
    page_number = request.args.get("page", 1, int)
    current_category = request.args.get("current_category", 1, int)

    # flask_sqlalchemy.BaseQuery.paginate
    # https: // flask-sqlalchemy.palletsprojects.com/en/2.x/api /?highlight = basequery
    # paginate returns a generator
    questions = Question.query.paginate(
        page_number,
        QUESTIONS_PER_PAGE,
        ERROR_OUT,
        MAX_QUESTIONS_PER_PAGE
    )
    categories = Category.query.all()
    format_categories = {
        str(Category.format(category)['id']): Category.format(category)['type']
        for category in categories
    }

    formatted_questions = [
        Question.format(question)
        for question in questions.items
    ]

    return jsonify({
        "questions": formatted_questions,
        "current_category": current_category,
        "categories": format_categories,
        "total_questions": questions.total
    })
