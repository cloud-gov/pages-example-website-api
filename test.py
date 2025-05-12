import os
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
import psycopg2
from psycopg2.extras import RealDictCursor
from psycopg2.pool import ThreadedConnectionPool

# Test app
app = FastAPI()

# Create single connection pool / Test values
pool = ThreadedConnectionPool(
    minconn=1,
    maxconn=5,
    host='localhost',
    user='pguser',
    password='pgpassword',
    database='app_db'
)

# Context manager for DB connections
class DBConnectionManager:
    def __enter__(self):
        self.connection = pool.getconn()
        return self.connection
    
    def __exit__(self, exc_type, exc_value, exc_traceback):
        if self.connection:
            pool.putconn(self.connection)
            
# Function to test
@app.get("/get_user")
def get_user():
    with DBConnectionManager() as connection:
        cursor = connection.cursor(cursor_factory=RealDictCursor)
        query = "SELECT * FROM users LIMIT 1"
        cursor.execute(query)
        user = cursor.fetchone()
        cursor.close()
        
        if user:
            return user
        else:
            return {"message": "No users found!"}, 400
        
# Test Client
client = TestClient(app)

# Test the get_user function
def test_get_user():
    response = client.get("/get_user")
    
    # Success Response
    assert response.status_code == 200
    
    # Response contains user data
    user_data = response.json()
    assert "id" in user_data
    assert "name" in user_data
    assert "created_on" in user_data
    
    # Name pattern check
    assert user_data["name"].startswith("User")
    
    # Cleanup function / Close connection pool
    @pytest.fixture(scope="session", autouse=True)
    def cleanup():
        yield
        if pool:
            pool.closeall()