from flask import Flask, render_template
import logging
app = Flask(__name__)
app.config.from_pyfile('config.py', silent=True)
from app.db import get_db

@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)