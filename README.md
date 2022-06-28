# Trivia App

Trivia is a challenge created by udacity to test students on their understanding of various full-stack concepts.

It was built using:

* react for the frontend
* flask for the backend

## Quickstart

### Install

1. **For the frontend:**

* Navigate to the frontend folder and run 
`npm install`

2. **For the backend:**
* Navigate to the backend folder
* Create your virtual environment, use [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/) as a guide
* After creating and activating your virtual environment, to install the required packages, use
`pip install -r requirements.txt`

### Seting up the Database

* Using postgres, create a database using the commands on psql:
`CREATE DATABASE trivia;`

* To create the tables, copy the path to the trivia.psql file and use the following command:
`\i c:/path_to_trivia.psql/trivia.psql`

### Run the Servers

**Both servers have to be running, preferrably the backend server first followed by the frontend**

* From the backend directory run the following commands:
```
set FLASK_APP=flaskr
set FLASK_ENV=development
flask run
```

* From the frontend directory run the following command:
`npm start`

### API 

These are the various routes that can be accessed once the servers are all running:

**GET '/categories'**

* Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category.
* Request Arguments: **None**
* Returns: **An object with a single key, categories, that contains an object of id: category_string key: value pairs.**
 ```
{
  "1": "Science",
  "2": "Art",
  "3": "Geography",
  "4": "History",
  "5": "Entertainment",
  "6": "Sports"
}
 ```


**GET '/questions?page=${integer}'**

* Fetches a paginated set of questions, a total number of questions, all categories and current category string.
* Request Arguments: **page - _integer_**
* Returns: **An object with 10 paginated questions, total questions, object including all categories, and current category string**
 ```
{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "currentCategory": "Entertainment",
  "questions": [
    {
      "answer": "Apollo 13",
      "category": 5,
      "difficulty": 4,
      "id": 2,
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    }
    ],
     "totalQuestions": 10
}
 ```


 **GET '/categories/${id}/questions'**

* Fetches questions for a cateogry specified by id request argument.
* Request Arguments: **id - _integer_**
* Returns: **An object with questions for the specified category, total questions, and current category string** 
```
{
  "currentCategory": "Science",
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
    }
  ],
  "totalQuestions": 2
}
```


 **DELETE '/questions/${id}'**

* Deletes a specified question using the id of the question.
* Request Arguments: **id - _integer_**
* Returns: **An object with the id of the deleted question, message(string) and success (boolean value)**
```
{
  "id": 19,
  "message": "You just deleted a question",
  "success": true
}
```


**POST '/play'**

* Sends a post request in order to get the next question.
* Request Body: 
```
{
    'previous_questions': [4,5,6,9,10,11,12,13,14,15],
    'quiz_category': {'type': 'click', 'id': 0}
}
 ```

 > NOTE: The quiz_category dictionary above is what is used when the user clicks all, if a _specific category_ is picked, the type would be the name of the category and the id would be the id of such category in the database

* Returns: **A single new question object**
```
{
  "question": {
    "answer": "Drake",
    "category": 5,
    "difficulty": 2,
    "id": 25,
    "question": "Who's is the biggest artist with Universal?"
  }
}
```


**POST '/questions'**

* Sends a post request in order to add a new question.
* Request Body: 

```
{
    'answer': 'Nigeria',
    'difficulty': '1',
    'category': '3',
    'question': 'What is the most populous African country?'
}
 ```

* Returns: **An object with the id of the new question, a message(string) and success (boolean)**
{
  "id": 27,
  "message": "You have created a new question",
  "success": true
}


**POST '/questions/search'**

* Sends a post request in order to search for a specific question by search term.
* Request Body: 

```
{
    "searchTerm": "What is the heaviest organ in the human body?"
}
 ```

* Returns: **Any array of questions, a number of totalQuestions that met the search term and the current category string**
{
  "currentCategory": "Science",
  "questions": [
    {
      "answer": "The Liver",
      "category": 1,
      "difficulty": 4,
      "id": 20,
      "question": "What is the heaviest organ in the human body?"
    }
  ],
  "totalQuestions": 1
}
