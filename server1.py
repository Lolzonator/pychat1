import time
from datetime import datetime
from flask import Flask, request
from werkzeug.exceptions import abort

app = Flask(__name__)

#TODO: база данных на стороне сервера с очисткой при достижении определённого размера
database = []


@app.route("/")
def hello():
    return "Добро пожаловать, ептель!! <a href='/status'>Статус сервера</a>"


@app.route("/status")
def status():

    return {
        'status': True,
        'name': 'ULTIMATE MESSENGER',
        'time': datetime.now(),
        'database_msgs': len(database),
    }

@app.route("/messages")
def get_messages():
    print(type(request.args['after']))
    try:
        after = float(request.args['after'])
    except:
        return abort(400)
    messages = []
    for message in database:
        if message['time'] > after:
            messages.append(message)

    return {'messages': messages[:50]}


@app.route("/send", methods=['POST'])
def send_message():
    data = request.json

#TODO: вставка IP  в выводимое сообщение

    if not isinstance(data, dict):
        return abort(400)
    if 'name' not in data or 'text' not in data:
        return abort(400)

    name = data['name']
    text = data['text']

    if not isinstance(name, str) or not isinstance(text, str):
        return abort(400)
    if not (0 < len(name) <= 16):
        return abort(400)
    if not (0 < len(text) <= 300):
        return abort(400)

    message = {
        'name': name,
        'text': text,
        'time': time.time()
    }

    database.append(message)

    print(database)
    return {'ok': True}




app.run()
