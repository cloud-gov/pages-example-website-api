import psycopg2
import os
from flask import Flask, jsonify
from cfenv import AppEnv
from psycopg2.extras import RealDictCursor
from flask_cors import CORS


app = Flask(__name__)
app_env = AppEnv()
CORS(app, origins=['https://federalist-31c21015-f923-4733-95df-2e979da3e393.sites.pages.cloud.gov'], headers=['Content-Type'], methods=['GET'])

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
    
    query = 'SELECT * FROM fdic_banks LIMIT 15'
    cursor.execute(query)
    
    rows = cursor.fetchall()
    cursor.close()
    
    return jsonify(rows)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port)

