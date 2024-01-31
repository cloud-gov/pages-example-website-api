import psycopg2
import os
from flask import Flask, jsonify
from cfenv import AppEnv
from psycopg2.extras import RealDictCursor


app = Flask(__name__)
app_env = AppEnv()

port = int(os.getenv('PORT', 8080))
    
aws_rds = app_env.get_service(name='hurricane')
    
cnx = psycopg2.connect(
    host=aws_rds.credentials.get('host'),
    user=aws_rds.credentials.get('username'),
    passwd=aws_rds.credentials.get('password'),
    database=aws_rds.credentials.get('name'),
    port=aws_rds.credentials.get('port'),
)
@app.route('/', methods=['GET'])
def hello():
    return 'There is a table right behind this door!'


# DB operations/ insert app path from cloud.gov, changed route from '/cfpyapi.app.cloud.gov -> '/get_gif'
@app.route('/get_table', methods=['GET'])
def get_gif():
    cursor = cnx.cursor(cursor_factory=RealDictCursor)
    
    # Execute SELECT query to retrieve table contents from cloud.gov
    query = 'SELECT * FROM fdic_banks'
    cursor.execute(query)
    
    # Fetch result
    rows = cursor.fetchall()
    cursor.close()
    
    return jsonify(rows)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port)

