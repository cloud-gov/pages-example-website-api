import psycopg2
import os
from flask import Flask, jsonify
from cfenv import AppEnv
from psycopg2.extras import RealDictCursor
from flask_cors import CORS


app = Flask(__name__)
app_env = AppEnv()
CORS(app, origins=['https://federalist-c8f0d18e-b710-44dc-9412-4b4f26efb0a3.sites.pages.cloud.gov, http://localhost:8080'], headers=['Content-Type'], methods=['GET'])

port = int(os.getenv('PORT', 8080))
    
aws_rds = app_env.get_service(name='hurricane')
    
connection = psycopg2.connect(
    host=aws_rds.credentials.get('host'),
    user=aws_rds.credentials.get('username'),
    password=aws_rds.credentials.get('password'),
    database=aws_rds.credentials.get('name'),
    port=aws_rds.credentials.get('port'),
)
@app.route('/', methods=['GET'])
def hello():
    return 'There is a table right behind this door!'

@app.route('/get_table', methods=['GET'])
def get_table():
    cursor = connection.cursor(cursor_factory=RealDictCursor)
    
    # Execute SELECT query to retrieve table contents from cloud.gov
    query = 'SELECT * FROM fdic_banks'
    cursor.execute(query)
    
    # Fetch result
    rows = cursor.fetchall()
    cursor.close()
    
    return jsonify(rows)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port)

