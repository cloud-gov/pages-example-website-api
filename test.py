import os
import psycopg2
from flask import Flask, jsonify
from cfenv import AppEnv
from psycopg2.extras import RealDictCursor
from psycopg2.pool import ThreadedConnectionPool
from flask_cors import CORS

origin = os.getenv("ORIGIN")
port = int(os.getenv("PORT", 8080))

app = Flask(__name__)
CORS(app, origins=origin)

connection_pool = ThreadedConnectionPool(
    minconn=1,
    maxconn=os.getenv('DB_MAX_CONNECTIONS'),
    host=os.getenv('DB_HOST'),
    user=os.getenv('DB_USER'),
    password="pgpassword",
    database="app_db",
)


def getconnection():
    return connection_pool.getconn()

#Returns connection to pool for reuse
def returnconnection(db_connection, close=False):
    connection_pool.putconn(db_connection, close=close)
    

@app.route("/", methods=["GET"])
def hello():
    try:
        return "There is a table right behind this door!"
    except Exception as error:
        return jsonify({"error": str(error)}), 500
    
# Test query
@app.route("/get_user", methods=["GET"])
def get_user():
    db_connection = None
    try:
        db_connection = getconnection()
        cursor = db_connection.cursor(cursor_factory=RealDictCursor)
        
        query = "SELECT * FROM users LIMIT 1"
        cursor.execute(query)
        
        user = cursor.fetchone()
        cursor.close()
        
        if user:
            return jsonify(user)
        else:
            return jsonify({"message": "No users found"}), 404
        
    except Exception as error:
        return jsonify({"error": str(error)}), 500
    finally:
        if db_connection:
            returnconnection(db_connection)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=port, threaded=True)