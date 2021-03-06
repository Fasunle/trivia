


from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask_cors import CORS

from config import (
    ALLOWED_LIST,
    SQLALCHEMY_DATABASE_URI
)
from flaskr.controllers.question import question_controller
from flaskr.controllers.category import categories_controller
from models import setup_db

# load environment variables
load_dotenv(".env")

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    
    # database entrypoint
    setup_db(app, SQLALCHEMY_DATABASE_URI)
    
    # routes
    app.register_blueprint(question_controller, url_prefix='/api/')
    app.register_blueprint(categories_controller, url_prefix='/api/')

    """
    Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    """
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    """
    Use the after_request decorator to set Access-Control-Allow
    """
    @app.after_request
    def set_access_controls(response):

        if str(request.origin) in ALLOWED_LIST:

            response.headers.add('Access-Control-Allow-Origin',
                                 request.origin)

            response.headers.add('Access-Control-Allow-Credentials', 'true')

            response.headers.add(
                'Access-Control-Allow-Headers', 'Content-Type')

            response.headers.add(
                'Access-Control-Allow-Headers', 'Cache-Control')

            response.headers.add(
                'Access-Control-Allow-Headers', 'X-Requested-With')

            response.headers.add(
                'Access-Control-Allow-Headers', 'Authorization')

            response.headers.add('Access-Control-Allow-Methods',
                                 'GET, POST, OPTIONS, PUT, DELETE')

        return response

    """
    Create an endpoint to handle GET requests
    for all available categories.
    """

    """
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    """

    """
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """

    """
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    """

    """
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """

    """
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """

    """
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    """

    """
    Create error handlers for all expected errors
    including 404 and 422.
    """
    
    @app.errorhandler(404)
    def content_not_found(error):
        return (
            jsonify({"success": False, "error": 404, "message": "resource not found"}),
            404,
        )

    @app.errorhandler(422)
    def content_not_processable(error):
        return (
            jsonify({"success": False, "error": 422, "message": "unprocessable"}),
            422,
        )

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({"success": False, "error": 400, "message": "bad request"}), 400
    
        
    @app.errorhandler(500)
    def server_error(error):
        return jsonify({"success": False, "error": 500, "message": "Server Error"}), 500


    return app
