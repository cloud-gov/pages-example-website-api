import mysql.connector
import os
from flask import Flask, jsonify
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
    cnx.autocommit = True
    cursor = cnx.cursor()
    
    # Execute SELECT query to retrieve GIF URL from cloud.gov
    query = 'SELECT gif_data FROM gifs'
    cursor.execute(query)
    
    # Fetch result
    result = cursor.fetchone()
    
    # Close cursor
    cursor.close()
    cnx.close()
    
    if result:
        gif_url = str(result[0])
        print('gif_url', gif_url)
        return jsonify({'gif_url': gif_url})
    else:
        print('message', 'GIF not found')
        return jsonify({'message': 'GIF not found'}), 404
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port)

