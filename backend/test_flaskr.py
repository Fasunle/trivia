from unicodedata import category
import unittest
import json
from flask_sqlalchemy import SQLAlchemy


from flaskr import create_app
from models import (setup_db, Question, Category)


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client()
        self.database_name = "trivia_test"
        self.database_path = "postgresql://{}/{}".format(
            'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after each test"""
        pass

    """
    Write at least one test for each test for successful operation and for expected errors.
    """

    def test_fetch_categories(self):
        """Fetch all categories
        
        test: 
            - status code 200 OK
            - expected dictionary
        """

        response = self.client.get("/api/categories")
        categories = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertListEqual(list(categories.keys()), ["categories"])

    def test_get_by_category(self):
        """Get questions by category
        """
        
        category_res = Category.query.first()
        mock_id = category_res.id
        
        response = self.client.get(f"/api/categories/{mock_id}/questions")
        
        questions = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(
            questions["questions"], list)

    
    def test_get_by_category_if_no_categoryId(self):
        """if no category id is specified, 
        """
        
        response = self.client.get("/api/categories/questions")
        res_data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 404)
        self.assertEqual(res_data["message"], "resource not found")
        
        
    def test_create_category(self):
        '''Create a new Category'''

        success_response_mock = "Category Created Successfully"
        failure_response_mock = "Category already exists!"
        payload = {
            'category': 'Marketing',
        }

        response = self.client.post('/api/categories', data=json.dumps(payload))

        # if category has been created already
        if response.status_code == 404:
            self.assertEqual(response.status_code, 404)
            self.assertEqual(json.loads(response.data), failure_response_mock)
            self.assertNotEqual(json.loads(response.data), "")
        
        # if category has not been created before
        elif response.status_code == 200:
            self.assertEqual(response.status_code, 200)
            self.assertEqual(json.loads(response.data), success_response_mock)
            self.assertNotEqual(json.loads(response.data), "")
            
    
    def test_update_category(self):
        '''Update a category'''
        
        # new type
        payload = {
            'type': 'Arts',
            "id": 2
        }
        
        success_response_mock = "Category Updated Successfully"
        failure_response_mock = "Category does not exist"
        wrong_data_response_mock  = "Category type is required"

        # get a random category
        category = Category.query.first()
        
        # make a PUT request
        response = self.client.put(f'/api/categories/{category.id}', data=json.dumps(payload))

        # response info
        status_code = response.status_code
        response_data = response.data.decode('utf-8')

        # if category cannot be updated!
        if status_code == 404:
            self.assertEqual(response_data, failure_response_mock)
            self.assertEqual(status_code, 404)
            self.assertNotEqual(response_data, "")
            
        # bad payload, client should send correct data to update
        elif status_code == 400:
            self.assertEqual(status_code, 400)
            self.assertEqual(response_data, wrong_data_response_mock)
            self.assertNotEqual(response_data, "")
        
        # if category has not been created before
        else:
            self.assertEqual(status_code, 200)
            self.assertEqual(response_data, success_response_mock)
            self.assertNotEqual(response_data, "")
        
    
    def test_delete_category(self):
        '''Delete a category'''    

        # get any random category
        category = Category.query.first()
        
        if category is None:
            return
        
        # delete the category
        response = self.client.delete(f"/api/categories/{category.id}")
        
        # check if the deletion was successful
        self.assertEqual(response.status_code, 200)
        
        # find the deleted category
        category = Category.query.get(category.id)
        
        # the category should be None already
        self.assertIsNone(category)

    def test_fetch_questions(self):
        """Get all questions and test that correct keys are returned for a given page
        """
        expected_keys = ["categories", "current_category",
                         "questions", "total_questions"]
        
        response = self.client.get('/api/questions')
        questions = json.loads(response.data)
        result_keys = list(questions.keys())

        self.assertEqual(response.status_code, 200)
        # by default, category type is 1
        self.assertEqual(questions["current_category"], 1)
        
        # return proper data format
        self.assertListEqual(result_keys, expected_keys)
        
        # questions type is list
        self.assertIsInstance(questions["questions"], list)
        self.assertNotIsInstance(questions["questions"], tuple)
        
        
    def test_fetch_questions_query_params(self):
        """Get all questions for a specific page and category via params
        """
        response = self.client.get('/api/questions?page=2&current_category=2')
        questions = json.loads(response.data)
        
        self.assertEqual(response.status_code, 200)
        # returns a current_category id
        self.assertEqual(questions["current_category"], 2)
        self.assertNotEqual(questions["current_category"], 1)
        # returns a list
        self.assertIsInstance(questions["questions"], list)
        self.assertNotIsInstance(questions["questions"], tuple)


    def test_delete_question(self):
        """Delete a question with a particular Id
        """
        question_raw= Question.query.first()
        question = Question.format(question_raw)
        mock_id = question['id']

        # delete a question
        response = self.client.delete(f"/api/questions/{mock_id}")
        # if successful, return 200 OK status code
        self.assertEqual(response.status_code, 200)
        
        
        # after deletion, fetch it again
        question_raw= Question.query.filter_by(id=mock_id).one_or_none()
        self.assertIsNone(question_raw)
        
        
    def test_delete_question_if_not_found(self):
        """Delete a question with a particular Id
        """
        question_raw= Question.query.first()
        question = Question.format(question_raw)
        mock_id = question['id']
        
        # delete the question
        self.client.delete(f"/api/questions/{mock_id}")

        # delete question that is already deleted
        response = self.client.delete(f"/api/questions/{mock_id}")

        # if failure, return 404 NotFound status code
        self.assertEqual(response.status_code, 404)

    def test_create_question(self):
        """Create question 
        test:
            - success status code (200 OK)
            - response message
        """
    
        response_mock = "Question created successfully!"
        payload = {
            'question': 'When are you submitting the project',
            'answer': "Today by 8:00am, June 17, 2022",
            'category': '4',
            'difficulty': 5
        }

        response = self.client.post('/api/questions', data=json.dumps(payload))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.data), response_mock)
        self.assertNotEqual(json.loads(response.data), "")
        
        
    def test_create_question_without_body(self):
        """if request body does not contain question, answer, difficulty, and category, return 404 status code with error message
        """
        response_msg_mock = "request object must have the following fields: question, answer, category, difficulty"
        payload = {
            'question': 'When are you submitting the project',
            'answer': "Today by 8:00am, June 17, 2022",
            'category': '4'
        }

        response = self.client.post('/api/questions', data=json.dumps(payload))

        self.assertEqual(response.status_code, 400)
        # response message
        self.assertNotEqual(response.get_data(True), "")
        self.assertEqual(response.get_data(True), response_msg_mock)
        
    def test_search_question(self):
        """Search for question by searchTerm in the request object
        
        test:
            - status code 200 OK
            - current_category
        """
        payload = {
            "searchTerm": "What"
        }

        response = self.client.post('/api/questions', data=json.dumps(payload))
        questions = json.loads(response.data)
        
        self.assertEqual(response.status_code, 200)
        self.assertIsNone(questions["current_category"])
        self.assertIsInstance(questions["questions"], list)
    
    def test_search_question_within_a_category(self):
        """Search for question by searchTerm in the request object
        
        test:
            - status code 200 OK
            - current_category
        """
        payload = {
            "searchTerm": "What"
        }

        response = self.client.post('/api/questions?current_category=2', data=json.dumps(payload))
        questions = json.loads(response.data)
        
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(questions["current_category"])
        self.assertEqual(int(questions["current_category"]), 2)
        self.assertIsInstance(questions["questions"], list)
    
    def test_quizzes(self):
        """If proper request object is specified, return a question object
        """
        question = Question.query.first()
        category = Category.query.filter_by(id=question.category).first()
        payload = {
            "previous_questions": [],
            "quiz_category": {
                "id": category.id,
                "type": category.type
            }
        }
        response = self.client.post('/api/quizzes', data=json.dumps(payload))
        result = json.loads(response.data)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(result.keys()), ["question"])

    def test_quizzes_if_not_formatted_well(self):
        """If data is not formatted as below, this test ensures that the format is adhere to.
        
            payload = {
                "previous_questions": [],
                "quiz_category": {
                    "id": 1,
                    "type": "Science"
                }
            }
        """

        payload = {
            "previous_questions": [],
        }
        response = self.client.post('/api/quizzes', data=json.dumps(payload))

        self.assertEqual(response.status_code, 400)
        
# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
