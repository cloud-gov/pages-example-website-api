import mysql.connector
import flask import Flask, jsonify

app = Flask(__name__)

# Get mysql creds from cloud.gov/import cloud.gov env vars
mysql_credentials = {
    'host': os.environ['MYSQL_HOST'],
    'port': os.environ['MYSQL_PORT'],
    'user': os.environ['MYSQL_USER'],
    'password': os.environ['MYSQL_PASSWORD'],
    'database': os.environ['MYSQL_DATABASE'],
}

# connect to DB
connection = mysql.connector.connect(**mysql_credentials)

# DB operations/ insert app path from cloud.gov
@app.route('/app/gif', methods=['GET'])
def get_gif():
    cursor = connection.cursor()
    
    # Execute SELECT query to retrieve GIF URL from cloud.gov
    query = 'SELECT gif_data FROM pages_content'
    cursor.execute(query)
    
    # Fetch result
    result = cursor.fetchone()
    
    # Close cursor
    cursor.close()
    
    if result:
        gif_url = result[0]
        return jsonify({'gif_url': gif_data})
    else:
        return jsonify({'message': 'GIF not found'})
    
    if __name__ == '__main__':
        app.run()

