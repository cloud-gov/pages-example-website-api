import mysql.connector
import os
from flask import Flask, jsonify
from cfenv import AppEnv


app = Flask(__name__)
app_env = AppEnv()

port = int(os.getenv('PORT', 8080))
    
aws_rds = app_env.get_service(name='lightening-db')
    
connection = mysql.connector.connect(
    host=aws_rds.credentials.get('host'),
    user=aws_rds.credentials['username'],
    passwd=aws_rds.credentials.get('password'),
    database=aws_rds.credentials.get('name'),
    port=aws_rds.credentials.get('port'),
)
 

# DB operations/ insert app path from cloud.gov
@app.route('/get_gif', methods=['GET'])
def get_gif():
    connection.autocommit = True
    cursor = connection.cursor()
    
    # Execute SELECT query to retrieve GIF URL from cloud.gov
    query = 'SELECT gif_data FROM pages_content'
    cursor.execute(query)
    
    # Fetch result
    result = cursor.fetchone()
    
    # Close cursor
    cursor.close()
    connection.close()
    
    if result:
        gif_url = result[0]
        return jsonify({'gif_url': gif_url})
    else:
        return jsonify({'message': 'GIF not found'})
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port)

