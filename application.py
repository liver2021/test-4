from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import OperationalError
from sqlalchemy import text


import os

application = Flask(__name__)

application.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres1234@database-2.cal68me0ewga.us-east-1.rds.amazonaws.com:5432/database-2'
application.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(application)



@application.route('/')
def hello_world():
    try:
        db.session.execute(text('SELECT 1'))
        message = "✅ Successfully connected to the PostgreSQL database."
    except OperationalError as e:
        message = f"❌ Failed to connect to the PostgreSQL database: {e}"
    return render_template('hello.html', message=message)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    application.run(host='0.0.0.0', port=port)
