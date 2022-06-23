from json import dumps, loads
from flask import jsonify, request

from flaskr.controllers import categories_controller
from models import Category
from models import Question


@categories_controller.route('/categories')
def fecth_categories():
    """Fetch all categories

    Returns:
        dict: a key-value {'id':'type'}
    """
    all_categories = Category.query.all()
    return {
        "categories": {
            Category.format(category)['id']:  Category.format(category)['type']
            for category in all_categories
        }
    }


@categories_controller.route('/categories/<int:id>/questions')
def get_by_category(id):
    """Get all questions given a category id

    Args:
        id (int): category id

    Returns:
        result: {
            "questions": questions,
            "current_category": current_category,
            "total_questions": total_questions
        }
    """

    # get the category type
    current_category = Category.format(Category.query.get(id)).get("type")

    # get all questions in the category
    questions = Question.query.filter_by(category=id).all()

    # get the questions count
    total_questions = Question.query.filter_by(category=id).count()

    # format the questions
    questions = [
        Question.format(question)
        for question in questions
    ]

    result = {
        "questions": questions,
        "current_category": current_category,
        "total_questions": total_questions
    }
    return jsonify(result)


@categories_controller.route("/categories", methods=["POST"])
def create_category():
    '''Create a new Category if not already present'''
    
    # parse data
    data = loads(request.data)
    category_type = data.get("category")
    
    # check if the category doesn't already exist
    check = Category.query.filter_by(type=category_type).all()
    
    if check is not []:
        return "Category already exists!", 400
    else:
        # category = Category(category_type).insert()
        return "Category Created Successfully", 200


@categories_controller.route("/categories/<int:id>", methods=["PUT"])    
def update_category(id):
    '''Update a category'''

    data = loads(request.data)
    category_type = data.get("type")

    if category_type is None:
        return "Category type is required", 400
    
    # find the category
    category = Category.query.get(id)

    if category is None:
        return "Category does not exist", 404
    
    # update the category
    new_category = Category(category_type)
    new_category.id = id
    new_category.update()
    
    return "Category Updated Successfully", 200
    
    
    
@categories_controller.route("/categories/<int:id>", methods=["DELETE"])
def delete_category(id):
    '''Delete a category'''
    
    # find if the category exist
    category = Category.query.get(id)
    
    # if exists, delete
    if category is not None:
        Category.delete(category)
        return "Category with id: {id} was deleted!", 200
    
    # else, return a message
    else:
        return "Category with id: {id} does not exist", 400