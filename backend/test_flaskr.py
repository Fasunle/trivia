import os
from typing import Literal
import unittest
import json
from urllib import response
from flask import (request, jsonify)
from flask_sqlalchemy import SQLAlchemy

from flaskr.controllers.question import fetch_questions
from flaskr.controllers.category import (fecth_categories, get_by_category)

from flaskr import create_app
from models import setup_db, Question, Category


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
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """

    def test_fetch_categories(self):

        categories = fecth_categories()

        expected_categories_1 = {
            "categories": {
                1: "Science",
                2: "Art",
                3: "Geography",
                4: "History",
                5: "Entertainment",
                6: "Sports"
            }
        }
        expected_categories_2 = {
            "categories": {
                1: "Science",
                2: "Art",
                3: "Geography",
                4: "History",
                5: "Entertainment"
            }
        }

        self.assertEqual(categories, expected_categories_1)
        self.assertNotEqual(categories, expected_categories_2)

    def test_get_by_category(self):
        """Get questions by category
        """
        
        science_mock_id = 1
        geography_mock_id = 3
        
        science_response = self.client.get(f"/api/categories/{science_mock_id}/questions")
        geography_response = self.client.get(f"/api/categories/{geography_mock_id}/questions")
        
        science_category = json.loads(science_response.data)
        geography_category = json.loads(geography_response.data)

        # science test
        self.assertEqual(science_category["current_category"], "Science")
        self.assertIsInstance(
            science_category["questions"], list)
        self.assertNotEqual(science_category["current_category"], "Geography")
        
        # geography test
        self.assertIsInstance(
            geography_category["questions"], list)
        self.assertEqual(
            geography_category["current_category"], "Geography")
    
    def test_get_by_category_if_no_categoryId(self):
        """if no category id is specified, 
        """
        
        response = self.client.get("/api/categories/questions")
        
        self.assertEqual(response.data, 200)

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


    def test_delete_question_if_found(self):
        """Delete a question with a particular Id
        """
        mock_id = 26

        # delete a question
        response = self.client.delete(f"/api/questions/{mock_id}")
        # if successful, return 200 OK status code
        self.assertEqual(response.status_code, 200)
        
    def test_delete_question_if_not_found(self):
        """Delete a question with a particular Id
        """
        mock_id = 23

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
        
        payload = {
            "previous_questions": [],
            "quiz_category": {
                "id": 1,
                "type": "Science"
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
