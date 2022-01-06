import sqlite3

import flask
from flask import abort, request, Response
from flask_cors import CORS
import json
import webbrowser

from model.student import Student
from controller import database_controller
import apisecrets

app = flask.Flask(__name__)
app.config["DEBUG"] = True
app.config['CORS_HEADERS'] = 'Content-Type'
# Implementacija ce biti na serveru, pa origins treba korigovati u "*" nakon zavrsetka testiranja
cors = CORS(app, resources={r"/foo": {"origins": "*"}})

students = []


@app.route('/api/v1/students', methods=['GET'])
def get_students():
    try:
        response = json.dumps(
            [Student(item).__dict__ for item in list(database_controller.get_students())],
            ensure_ascii=False
        )
        return Response(response, mimetype='application/json')
    except Exception as x:
        error = {
            'error': "Fetch exception",
            'detailedMessage': str(x)
        }
        return Response(json.dumps(error, ensure_ascii=False), mimetype='application/json')


@app.route('/api/v1/student/<string:student_id>', methods=['GET'])
def get_student(student_id):
    try:
        student_id = student_id.replace("-", "/")
        student = Student(database_controller.get_student(student_id))
        return Response(json.dumps(student.__dict__, ensure_ascii=False), mimetype='application/json')
    except Exception as x:
        error = {
            'error': "Fetch exception",
            'detailedMessage': str(x)
        }
        return Response(json.dumps(error, ensure_ascii=False), mimetype='application/json')


@app.route('/api/v1/students', methods=['POST'])
def write_student():
    if request.json is None:
        error = {
            'error': "No body defined",
            'description': "Please send body in the exact order as specified per the documentation"
        }
        return Response(json.dumps(error, ensure_ascii=False), mimetype='application/json')
    elif list(request.json.keys()) != Student.fields:
        error = {
            'error': "Wrong body",
            'description': "Please send body in the exact order as specified per the documentation"
        }
        return Response(json.dumps(error, ensure_ascii=False), mimetype='application/json')
    elif [type(item) for item in list(request.json.values())] != Student.types:
        error = {
            'error': "Wrong body",
            'description': "Please pay attention to the type of data you're sending (string vs integer)"
        }
        return Response(json.dumps(error, ensure_ascii=False), mimetype='application/json')
    else:
        try:
            s = Student(request.json)
            database_controller.insert_student(s)
            return Response(json.dumps({"status": "ok"}, ensure_ascii=False), mimetype='application/json')
        except sqlite3.IntegrityError as x:
            error = {
                'error': "Integrity error",
                'description': "Most likely that this studentID exists - try another one"
            }
            return Response(json.dumps(error, ensure_ascii=False), mimetype='application/json')
        except Exception as x:
            error = {
                'error': "Invalid request",
                'description': str(x)
            }
            return Response(json.dumps(error, ensure_ascii=False), mimetype='application/json')


@app.route('/api/v1/docs', methods=['GET'])
def get_docs():
    github_docs_link = "https://github.com/nedkuj-fsk/fsk-adresar-api/blob/master/README.md"
    webbrowser.open_new_tab(github_docs_link)
    response = {
        "status": "Redirected",
        'message': "If not redirected automatically, click link below.",
        'link': github_docs_link
    }
    return Response(json.dumps(response, ensure_ascii=False), mimetype='application/json')


@app.route(f'/api/v1/db/create/{apisecrets.ADMIN_CODE}', methods=['GET'])
def create_db():
    database_controller.createDatabase()
    response = {
        "status": "ok"
    }
    return Response(json.dumps(response, ensure_ascii=False), mimetype='application/json')


@app.route(f'/api/v1/db/empty/{apisecrets.ADMIN_CODE}', methods=['GET'])
def empty_db():
    database_controller.empty_database()
    response = {
        "status": "ok"
    }
    return Response(json.dumps(response, ensure_ascii=False), mimetype='application/json')


app.run(host='0.0.0.0', port=20177)
