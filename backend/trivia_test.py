import unittest
import json
from flaskr import create_app
from models import setup_db, Question, Category

class TriviaTestCase(unittest.TestCase):

    def setUp(self) -> None:

        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = 'postgresql://{}/{}'.format('postgres:seyi@localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        self.new_question = {
            'answer': 'Nigeria',
            'difficulty': '1',
            'category': '3',
            'question': 'What is the most populous African country?'
        }

        self.play = {
            'previous_questions': [4,5,6,9,10,11,12,13,14,15],
            'quiz_category': {'type': 'click', 'id': 0}
        }

        self.search_term = {"searchTerm": "What is the heaviest organ in the human body?"}

    def tearDown(self) -> None:
        pass


    def test_pagination_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(len(data['questions']))
        self.assertTrue(data['totalQuestions'])
        self.assertTrue(len(data['categories']))
        self.assertTrue(data['currentCategory'])


    def test_delete_question(self):
        question_id = 27
        res = self.client().delete(f'/questions/{question_id}')
        data = json.loads(res.data)

        question = Question.query.filter(Question.id == question_id).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['id'], question_id)
        self.assertEqual(question, None)

    # def test_create_new_question(self):
    #     res = self.client().post("/questions", json=self.new_question)
    #     data = json.loads(res.data)
    #     question = Question.query.order_by(Question.id).filter((Question.question.ilike(f'%What is the most populous African country?%'))).all()

    #     print(question[0].id)

    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data["success"], True)
    #     self.assertEqual(data["id"], question[0].id)

    def test_search_question(self):
        res = self.client().post("questions/search", json=self.search_term)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(len(data['questions']))
        self.assertEqual(data['totalQuestions'], 1)
        self.assertEqual(data['currentCategory'], "Science")

    def test_get_category_questions(self):
        category_id = 1
        res = self.client().get(f"/categories/{category_id}/questions")
        data = json.loads(res.data)

        category = Category.query.filter(Category.id==category_id)
        questions = Question.query.filter(Question.category==category_id)
        formatted_questions = [ question.format() for question in questions ]

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['currentCategory'], "Science")
        self.assertEqual(data['totalQuestions'], len(formatted_questions))
        self.assertTrue(len(data['questions']))

    def test_404_requesting_beyond_valid_page(self):
        res = self.client().get("/questions?page=1000")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Sorry, nothing found")

    def test_play_quiz(self):
        res = self.client().post('/play', json=self.play)
        data = json.loads(res.data)

        self.assertTrue(len(data['question']))
        self.assertNotIn(data['question']['id'], self.play['previous_questions'])

if __name__ == "__main__":
    unittest.main()