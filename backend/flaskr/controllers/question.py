import json
from flask import (
    abort,
    jsonify,
    request
)

from config import (
    ERROR_OUT,
    MAX_QUESTIONS_PER_PAGE
    QUESTIONS_PER_PAGE,
)
from flaskr.controllers import (
    get_random_integer,
    question_controller
)
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
        return f"Question with id: {id} was not found", 404
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

    # CREATE NEW QUESTIONS
    question = data.get('question')
    difficulty = data.get('difficulty')
    category = data.get('category')
    answer = data.get('answer')
    
    if search_term:
        return search_question(search_term, current_category)

    
    elif question != None and answer != None and category != None and difficulty != None:

        _question = Question(
                question, 
                answer,
                category, 
                difficulty
            )

        Question.insert(_question)   # create the question
        return jsonify("Question created successfully!")
    
    return "request object must have the following fields: question, answer, category, difficulty", 400


def search_question(search_term, current_category):
    # get the category
    # category = Category.query.get(current_category)
    
    # return empty if the category is not found
    if search_term is None:
        return jsonify({
            "questions": [],
            "current_category": current_category,
            "total_questions": 0
        })

    # category_id = category.id
    questions_like = Question.question.like(f"%{search_term}%")
    
    # if category is not None, then get the id
    if current_category != None:
        questions = Question.query.filter_by(
            category=current_category
        ).filter(
            questions_like
        ).all()
    else:
        questions = Question.query.filter(
            questions_like
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


@question_controller.route("/quizzes", methods=["POST"])
def quizzes():
    """Generate a random question and when the questions list is exhusted, it would restart

    Returns:
        json: question object
    """
    data = json.loads(request.data)
    quiz_category = data.get("quiz_category")

    if  quiz_category == None or data.get("previous_questions") == None:
        print("Wrong data format. 'quiz_category' objet must be specified!")
        abort(400)
    else:
        category_id = data["quiz_category"]["id"]
        category_type = data["quiz_category"]["type"]
    previous_question_ids = data["previous_questions"]

    # get the questions by category
    questions_by_category = []

    if category_id == 0 and category_type == "ALL":
        questions_by_category = Question.query.all()
    else:
        questions_by_category = Question.query.filter(
            Question.category == category_id).all()

    # filter off the previous questions
    questions = list(
        filter(lambda x: x.id not in previous_question_ids,
               questions_by_category or [])
    )

    # generate random integer =<  len(questions)
    if len(questions) != 0:
        random_question_index = get_random_integer(len(questions))
        random_question = Question.format(questions[random_question_index])

    # if the category does not contain any question
    else:
        return "This category does not have any question.", 404

    return jsonify({
        "question": random_question
    })
