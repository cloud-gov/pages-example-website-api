import os
import atexit
from flask import Flask, jsonify
from cfenv import AppEnv
from flask_cors import CORS
from psycopg_pool import ConnectionPool
from psycopg.rows import dict_row
from psycopg.errors import OperationalError

origin = os.getenv("ORIGIN")
port = int(os.getenv("PORT", 8080))

app = Flask(__name__)
CORS(app, origins=origin)

app_env = AppEnv()
aws_rds = app_env.get_service(name="example-website-api-database")

# Set up pool as a function so in the case it dies we can recreate it 
def setup_connection_pool():
    
    database_url = os.getenv("DATABASE_URL")
    
    pool = ConnectionPool(
        conninfo=database_url,
        min_size=1,
        max_size=20,
    )
    return pool

# Immediately create pool at module import 
connection_pool = setup_connection_pool()


# Recreate pool if it dies
def recreate_connection_pool():
    global connection_pool
    
    # Close if it exists
    if connection_pool is not None:
        try:
            connection_pool.close()
        except Exception:
            pass
        
    # Create new pool   
    new_pool = setup_connection_pool()
    
    # Update variable
    connection_pool = new_pool
    
    atexit.register(connection_pool.close)
    
    return connection_pool

@app.route("/", methods=["GET"])
def hello():
    try:
        return "There is a table right behind this door!"
    except Exception as error:
        return jsonify({"error": str(error)}), 500

def fetch_fdic_banks(pool):
    with pool.connection() as conn:
        cursor = conn.cursor(row_factory=dict_row)
        cursor.execute("SELECT * FROM fdic_banks LIMIT 15")
        return jsonify(cursor.fetchall())

@app.route("/get_table", methods=["GET"])
def get_table():   
    global connection_pool
    try:
        # Using the method and not the pool itself as the context manager
        return fetch_fdic_banks(connection_pool)
    except OperationalError:
                
                
    #DB error, recreate pool
        connection_pool = recreate_connection_pool()
    
    # Use new pool
    try:
        return fetch_fdic_banks(connection_pool)
    except Exception as error:
        return jsonify({"error": "Database connection failed"}), 500
    
    except Exception as error:
        return jsonify({"error": str(error)}), 500
    
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=port, threaded=True)