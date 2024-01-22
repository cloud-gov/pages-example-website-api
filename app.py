import mysql.connector
import os
import tempfile
from flask import Flask, jsonify, send_file
from cfenv import AppEnv


app = Flask(__name__)
app_env = AppEnv()

port = int(os.getenv('PORT', 8080))
    
aws_rds = app_env.get_service(name='lightening-db')
    
cnx = mysql.connector.connect(
    host=aws_rds.credentials.get('host'),
    user=aws_rds.credentials.get('username'),
    passwd=aws_rds.credentials.get('password'),
    database=aws_rds.credentials.get('name'),
    port=aws_rds.credentials.get('port'),
)
@app.route('/', methods=['GET'])
def hello():
    return 'There is a GIF right behind this door!'


# DB operations/ insert app path from cloud.gov, changed route from '/cfpyapi.app.cloud.gov -> '/get_gif'
@app.route('/get_gif', methods=['GET'])
def get_gif():
    cursor = cnx.cursor()
    
    # Execute SELECT query to retrieve GIF URL from cloud.gov
    query = 'SELECT gif_data FROM gifs'
    cursor.execute(query)
    
    # Fetch result
    result = cursor.fetchone()
    
    if result:
        gif_data = result[0]
        with tempfile.NamedTemporaryFile(delete=False) as temp:
            temp.write(gif_data)
        
        return send_file(gif_data, mimetype='image/gif')
    else:
        return jsonify({'message': 'GIF not found'}), 404
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port)

