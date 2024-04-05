from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)


@app.route('/')
def index():
    return "<p>hello world</p>"

if __name__ == '__main__':
    app.run()