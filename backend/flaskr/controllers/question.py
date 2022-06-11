import json
from unicodedata import category
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


@question_controller.route('/questions')
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


@question_controller.route('/questions/<int:id>', methods=["DELETE"])
def delete_question(id):
    """Given a question id, delete the question

    Args:
        id (int): unique identifier of the question

    Returns:
        string: id of the deleted question if the deletion was successful.
        Otherwise, failure message is returned
    """
    # fetch a question with the id
    question = Question.query.get(id)
    # handle when the wrong id is passed
    if question == None:
        return f"Question with id: {id} was not found"
    else:
        Question.delete(question)

    return jsonify(f"Question with id: {id} was deleted")


@question_controller.route('/questions', methods=["POST"])
def create_question():
    """Create a question or search for a question

    Returns:
        string: Success message
    """
    # convert byte to dict
    # https://docs.python.org/3/library/json.html
    data = json.loads(request.data)

    # SEARCH QUESTIONS
    search_term = data.get("searchTerm")
    current_category = request.args.get("current_category")

    if search_term:
        print(current_category)
        return search_question(search_term, current_category)

    # CREATE NEW QUESTIONS

    question = Question(data['question'], data['answer'],
                        data['category'], data['difficulty'])

    Question.insert(question)   # create the question
    return jsonify("Question created successfully!")


def search_question(search_term, current_category):
    # get the category
    category = Category.query.filter_by(
        type=current_category
    ).first()

    # return empty if the category is not found
    if category is None:
        return jsonify({
            "questions": [],
            "current_category": current_category,
            "total_questions": 0
        })

    # if category is not None, then get the id
    category_id = category.id

    questions_like = Question.question.like(f"%{search_term}%")
    questions = Question.query.filter(
        questions_like
    ).filter_by(
        category=category_id
    ).all()

    questions_formatted = [
        Question.format(question)
        for question in questions
    ]

    result = {
        "questions": questions_formatted,
        "current_category": current_category,
        "total_questions": len(questions_formatted)
    }

    return jsonify(result)
