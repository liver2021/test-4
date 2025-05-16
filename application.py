from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import boto3
from sqlalchemy.exc import OperationalError
from sqlalchemy import text
import os
import json



application = Flask(__name__)
def get_secret():
    secret_name = "db/secret"  # Replace with your secret name
    region_name = "us-east-1"  # Replace with your region

    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    try:
        response = client.get_secret_value(SecretId=secret_name)
    except Exception as e:
        print("Failed to fetch secret:", e)
        raise e

    secret = json.loads(response['SecretString'])
    return secret

# Get credentials from Secrets Manager
creds = get_secret()
user = creds['username']
password = creds['password']
host = creds['host']
port = creds['port']
dbname = creds['dbname']
print("Hello this is Database Name:", dbname)

application.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{user}:{password}@{host}:{port}/{dbname}'
application.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(application)



@application.route('/')
def hello_world():
    try:
        with db.engine.connect() as connection:
            connection.execute(text('SELECT 1'))
            message = "✅ Successfully connected to the PostgreSQL database."

    except OperationalError as e:
        message = f"❌ Failed to connect to the PostgreSQL database: {e}"
    return render_template('hello.html', message=message)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    application.run(host='0.0.0.0', port=port)
