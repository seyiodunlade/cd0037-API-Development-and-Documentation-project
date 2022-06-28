# from crypt import methods
import os
from unicodedata import category
from urllib import response
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def get_categories():
    categories = Category.query.order_by(Category.id).all()
    formatted_categories = { category.id:category.type for category in categories }
    return formatted_categories


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    """
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    """
    
    CORS(app, resources={r"*": {'origins': '*'}})
    """
    @TODO: Use the after_request decorator to set Access-Control-Allow
    """
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PATCH, DELETE, OPTIONS')

        return response
    """
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    """
    @app.route('/categories', methods=['GET'])
    def categories():
        categories = get_categories()
        if len(categories) == 0:
            abort(404)

        print(get_categories()[1])
        return jsonify({'categories': categories})

    """
    @TODO:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.
    
    """
    @app.route('/questions', methods=['GET'])
    def questions():
        
         
        page = request.args.get('page', 1, type=int)
        questions = Question.query.order_by(Question.id).all()
        start = (page - 1) * QUESTIONS_PER_PAGE
        stop = start + QUESTIONS_PER_PAGE
        formatted_questions = [question.format() for question in questions[start:stop]]
        categories = get_categories()
        if len(formatted_questions) == 0:
            abort(404)

        # print(categories)
        # print(categories[formatted_questions[0]['category']])
        currentCategory = categories[formatted_questions[0]['category']]
        # print(f'CURRENT CATEGORY: {currentCategory}')
        
        return jsonify({
            'questions': formatted_questions,
            'totalQuestions': len(formatted_questions),
            'categories': categories,
            'currentCategory': currentCategory
        })

        
    """

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    """


    """
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    """

    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        print(question_id)
        try:
            question = Question.query.filter(Question.id == question_id).one_or_none()
            print(question)
            if question == None:
                abort(404)
        
            else:
                question.delete()
                print('You just deleted a question!!!!!')
                return jsonify({
                    'success': True,
                    'message': 'You just deleted a question',
                    'id': question.id
                })

        except Exception:
            abort(422)

    """

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """

    """
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    """

    @app.route('/questions', methods=['POST'])
    def create_question():
        try:
            request_data = request.get_json()
            question = request_data['question']
            answer = request_data['answer']
            difficulty = request_data['difficulty']
            category = request_data['category']

            new_question = Question(question,answer,category,difficulty)
            new_question.insert()

            return jsonify({
                'success': True,
                'message': 'You have created a new question',
                'id': new_question.id
            })

        except Exception:

            abort(422)

    """

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    """

    """
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    """

    @app.route('/questions/search', methods=['POST'])
    def search_question():

        request_data = request.get_json()
        search_term = request_data['searchTerm'] or ''
        print(f'SEARCH TERM --------- {search_term}')
        if search_term != '':

            result = Question.query.order_by(Question.id).filter((Question.question.ilike(f'%{search_term}%'))).all()
            formatted_result = [ question.format() for question in result ]
            currentCategory = formatted_result[0]['category']
            print(f'TYPE ----- {type(result)}')
            print(f'currentCategory --------- {currentCategory}')
            return jsonify({
                'questions': formatted_result,
                'totalQuestions': len(formatted_result),
                'currentCategory': get_categories()[currentCategory]
            })

        else:

            abort(400)


    """
    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """

    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    """

    @app.route('/categories/<int:category_id>/questions')
    def category_questions(category_id):

        category = Category.query.filter(Category.id==category_id)
        questions = Question.query.filter(Question.category==category_id)
        formatted_questions = [ question.format() for question in questions ]
        total_questions = len(formatted_questions)

        return jsonify({
            'questions': formatted_questions,
            'totalQuestions': total_questions,
            'currentCategory': category[0].type
        })


    """

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """


    """
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    """ 
    
    @app.route('/play', methods=['POST'])
    def play_quiz():
        
        request_data = request.get_json()
        print(f'REQUEST-DATA: {request_data}')
        prev_questions_list = request_data['previous_questions']
        category = request_data['quiz_category']['id']
        next_question_list = []
        formatted_question_list = []
        possible_questions_list = []


        if len(prev_questions_list) == 0:
            possible_questions_list = Question.query.filter(Question.category == category).all()
            if int(category) == 0:
                possible_questions_list = Question.query.all()
        else:
            possible_questions_list = Question.query.filter(Question.id.notin_(prev_questions_list)).filter(Question.category == category).all()
            if int(category) == 0:
                possible_questions_list = Question.query.filter(Question.id.notin_(prev_questions_list)).all()

        print(f'POSSIBLE QUESTIONS LIST: {possible_questions_list}')

        next_question_list = random.sample(possible_questions_list, k=1)

        print(f'NEXT QUESTION LIST: {next_question_list}')

        formatted_question_list = [question.format() for question in next_question_list]

        print(f'FORMATTED QUESTION LIST: {formatted_question_list}')

        return jsonify({
            'question': formatted_question_list[0]
            })

    """

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    """

    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'success': False,
            'error': 400,
            'message': 'Bad request'
        })

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 404,
            'message': "Sorry, nothing found"
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            'success': False,
            'error': 422,
            'message': 'This request could not be processed'
        }), 422

    return app

