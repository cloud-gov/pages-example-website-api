import psycopg2
import os
from flask import Flask, jsonify
from cfenv import AppEnv
from psycopg2.extras import RealDictCursor
from flask_cors import CORS

origin = os.getenv("ORIGIN")
port = int(os.getenv("PORT", 8080))

app = Flask(__name__)
CORS(app, origins=origin)

app_env = AppEnv()
aws_rds = app_env.get_service(name="example-website-api-databse")

def get_connection():
    connection = psycopg2.connect(
        host=aws_rds.credentials.get("host"),
        user=aws_rds.credentials.get("username"),
        password=aws_rds.credentials.get("password"),
        database=aws_rds.credentials.get("name"),
        port=aws_rds.credentials.get("port"),
)
    return connection

connection = get_connection()

@app.route("/", methods=["GET"])
def hello():
    return "There is a table right behind this door!"


@app.route("/get_table", methods=["GET"])
def get_table():
    if connection.closed:
        connection = get_connection()
    cursor = connection.cursor(cursor_factory=RealDictCursor)

    query = "SELECT * FROM fdic_banks LIMIT 15"
    cursor.execute(query)

    rows = cursor.fetchall()
    cursor.close()

    return jsonify(rows)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=port)
