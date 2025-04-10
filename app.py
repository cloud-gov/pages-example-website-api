import os
import psycopg2
from flask import Flask, jsonify
from cfenv import AppEnv
from psycopg2.extras import RealDictCursor
from psycopg2.pool import ThreadedConnectionPool
from psycopg2.pool import SimpleConnectionPool
from psycopg2 import pool
from flask_cors import CORS

origin = os.getenv("ORIGIN")
port = int(os.getenv("PORT", 8080))

app = Flask(__name__)
CORS(app, origins=origin)

app_env = AppEnv()
aws_rds = app_env.get_service(name="example-website-api-database")

# Uncomment after testing
"""
connection_pool = ThreadedConnectionPool(
    minconn=5,
    maxconn=20,
    host=aws_rds.credentials.get("host"),
    user=aws_rds.credentials.get("username"),
    password=aws_rds.credentials.get("password"),
    database=aws_rds.credentials.get("name"),
    port=aws_rds.credentials.get("port"),
)
"""


#Local Testing below
#connection_pool uses psycopg2 under the hood
connection_pool = ThreadedConnectionPool(
    minconn=5,
    maxconn=20,
    host="localhost",
    user="pguser",
    password="pgpassword",
    database="app_db",
    port=5432
)

# Retrieve connection from pool
# implement try/catch 1. check if this connected 2. get connection and if fails with error then reestablish connection pool and retry within catch
# ex. try return connection_pool.getconn() except -- and make sure it doesnt loop endlessly 
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


@app.route("/get_table", methods=["GET"])
def get_table():
    db_connection = None
    try:
        db_connection = getconnection()    
        cursor = db_connection.cursor(cursor_factory=RealDictCursor)

        query = "SELECT * FROM fdic_banks LIMIT 15"
        cursor.execute(query)

        rows = cursor.fetchall()
        cursor.close()

        # Specific to data from db to be converted to json
        return jsonify(rows)
    except Exception as error:
        # implement both error logs (app.logger) server way / dont stringify entire error to go back to user / replace 500 with "unexpected error occured"
        return jsonify({"error": str(error)}), 500
    finally: 
        if db_connection:
            returnconnection(db_connection)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=port, threaded=True)
