import os
import unittest
import json
from flask import request
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
        self.client = self.app.test_client
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
        """Executed after reach test"""
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

        expected_geography_result = {
            "current_category": "Geography",
            "questions": [
                {
                    "answer": "The Palace of Versailles",
                    "category": 3,
                    "difficulty": 3,
                    "id": 14,
                    "question": "In which royal palace would you find the Hall of Mirrors?"
                },
                {
                    "answer": "Agra",
                    "category": 3,
                    "difficulty": 2,
                    "id": 15,
                    "question": "The Taj Mahal is located in which Indian city?"
                },
                {
                    "answer": "Fasunle Kehinde Hussein",
                    "category": 3,
                    "difficulty": 1,
                    "id": 24,
                    "question": "What is your name?"
                }
            ],
            "total_questions": 3
        }

        expected_science_result = {
            "current_category": "Science",
            "questions": [
                {
                    "answer": "The Liver",
                    "category": 1,
                    "difficulty": 4,
                    "id": 20,
                    "question": "What is the heaviest organ in the human body?"
                },
                {
                    "answer": "Alexander Fleming",
                    "category": 1,
                    "difficulty": 3,
                    "id": 21,
                    "question": "Who discovered penicillin?"
                },
                {
                    "answer": "Blood",
                    "category": 1,
                    "difficulty": 4,
                    "id": 22,
                    "question": "Hematology is a branch of medicine involving the study of what?"
                }
            ],
            "total_questions": 3
        }

        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            science_category = json.loads(get_by_category(1).data)
            geography_category = json.loads(get_by_category(3).data)

        self.assertEqual(science_category["current_category"], "Science")
        self.assertListEqual(
            science_category["questions"], expected_science_result["questions"])
        self.assertEqual(
            science_category["total_questions"], expected_science_result["total_questions"])

        self.assertNotEqual(science_category["current_category"], "Geography")
        self.assertListEqual(
            geography_category["questions"], expected_geography_result["questions"])
        self.assertEqual(
            geography_category["total_questions"], expected_geography_result["total_questions"])

    def test_fetch_questions(self):
        """Get all questions and test that correct keys are returned for a given page
        """
        expected_keys = ["categories", "current_category",
                         "questions", "total_questions"]

        with self.app.test_request_context("/api/questions?page=1"):
            questions = json.loads(fetch_questions().data)
            page_count = int(request.args.get('page'))
            result_keys = list(questions.keys())

        self.assertListEqual(result_keys, expected_keys)
        self.assertEqual(1, page_count)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
