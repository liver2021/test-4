from flask import Flask, render_template
import os

application = Flask(__name__)

@application.route('/')
def hello_world():
    return render_template('hello.html')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    application.run(host='0.0.0.0', port=port)
