import numpy as np
from flask import Flask, request, jsonify
import pickle
import os
import uuid
from flask_cors import CORS

# configuration
DEBUG = True

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)

# Unpickle our model so we can use it!
if os.path.isfile("./model.pkl"):
  model = pickle.load(open("./model.pkl", "rb"))
else:
  raise FileNotFoundError

# model = pickle.load(open('model.pkl', 'rb'))

BOOKS = [
    {
        'id': uuid.uuid4().hex,
        'title': 'On the Road',
        'author': 'Jack Kerouac',
        'read': True,
        'price': '19.99'
    },
    {
        'id': uuid.uuid4().hex,
        'title': 'Harry Potter and the Philosopher\'s Stone',
        'author': 'J. K. Rowling',
        'read': False,
        'price': '9.99'
    },
    {
        'id': uuid.uuid4().hex,
        'title': 'Green Eggs and Ham',
        'author': 'Dr. Seuss',
        'read': True,
        'price': '3.99'
    }
]

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})

@app.route('/ping', methods=['GET'])
def ping_pong():
    return jsonify('pong')

@app.route('/salary', methods=['POST','GET'])
def predict():
    response_object = {'status': 'success'}
    if request.method == 'POST':
        int_features = [int(x) for x in request.get_json().values()]
        final_features = [np.array(int_features)]
        prediction = model.predict(final_features)
        output = round(prediction[0],2)
        prediction_text='Your Salary should be $ {}'.format(output)

        response_object['salary'] = prediction_text

        # int_features = [int(x) for x in sal ]
        # final_features = [np.array(int_features)]
        # prediction = model.predict(final_features)
        # output = round(prediction[0], 2)
        # response_object['salary'] = output
    else:
        #for get request (not required for predicting salary but kept for other uses)
        response_object['salary'] = 'enter correct'

    return jsonify(response_object)

    # int_features = [int(x) for x in request.form.values()]
    # final_features = [np.array(int_features)]
    # prediction = model.predict(final_features)

    # output = round(prediction[0], 2)


    # return render_template('index.html', prediction_text='Employee Salary should be $ {}'.format(output))

@app.route('/books', methods=['GET', 'POST'])
def all_books():
    response_object = {'status': 'success'}
    if request.method == 'POST':
        post_data = request.get_json()
        BOOKS.append({
            'id': uuid.uuid4().hex,
            'title': post_data.get('title'),
            'author': post_data.get('author'),
            'read': post_data.get('read'),
            'price': post_data.get('price')
        })
        response_object['message'] = 'Book added!'
    else:
        response_object['books'] = BOOKS
    return jsonify(response_object)

def remove_book(book_id):
    for book in BOOKS:
        if book['id'] == book_id:
            BOOKS.remove(book)
            return True
    return False

@app.route('/books/<book_id>', methods=['GET', 'PUT', 'DELETE'])
def single_book(book_id):
    response_object = {'status': 'success'}
    if request.method == 'GET':
        # TODO: refactor to a lambda and filter
        return_book = ''
        for book in BOOKS:
            if book['id'] == book_id:
                return_book = book
        response_object['book'] = return_book
    if request.method == 'PUT':
        post_data = request.get_json()
        remove_book(book_id)
        BOOKS.append({
            'id': uuid.uuid4().hex,
            'title': post_data.get('title'),
            'author': post_data.get('author'),
            'read': post_data.get('read'),
            'price': post_data.get('price')
        })
        response_object['message'] = 'Book updated!'
    if request.method == 'DELETE':
        remove_book(book_id)
        response_object['message'] = 'Book removed!'
    return jsonify(response_object)



if __name__ == '__main__':
    app.run()
