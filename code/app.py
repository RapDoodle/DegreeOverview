from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hello, World!'

@app.route("/add")
def add_user():
    # FIXME: Add new user code logic here
    return jsonify({
        'nickname':'uic02',
        'email':'12142819@qq.com',
        'role':'developer',
        'code':200
    })