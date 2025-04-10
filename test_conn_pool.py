# Focus on testing 2 functions from app, get_connection and return_connection. call those and can remove select queieries and things that work already
# can mock the data (call db query you tell it what data to return instead of it trying to connect to a db return, you predefine what client.query returns) fixture = connect to to preloaded docker db
import unittest
import os
import psycopg2
from psycopg2.pool import ThreadedConnectionPool
from psycopg2.extras import RealDictCursor
from flask import Flask

app = Flask(__name__)

connection_pool = ThreadedConnectionPool(
    minconn=2,
    maxconn=5,
    host="localhost",
    port=55401,
    dbname="postgres",
    user="ue3fe5f2if80sh84",
    password="owdqyw812gvhd0g5l3yxtmlym"
)

def getconnection():
    return connection_pool.getconn()

def returnconnection(db_connection, close=False):
    connection_pool.putconn(db_connection, close=close)
    
    #Check connection vailidity
    def is_connection_valid(db_connection):
        try:
            cursor = db_connection.cursor()
            cursor.execute("SELECT 1")
            cursor.close()
            return True
        except Exception:
            return False
        
class TestDatabaseConnection(unittest.TestCase):
    def test_get_connection(self):
        """Test that we get a connection from pool"""
        db_connection = getconnection()
        self.assertIsNotNone(db_connection, "Womp Womp Failed to get a connection from the pool")
        
    def test_connection_validity(self):
        """Test validity of pool connections"""
        db_connection = getconnection()
        self.assertTrue(is_connection_valid(db_connection), "Connection from pool is not valid")
        returnconnection(db_connection)
        
    def test_basic_query(self):
        db_connection = None
        try:
            db_connection = getconnection()
            cursor = db_connection.cursor()
            cursor.execute("SELECT 1 as test_value")
            result = cursor.fetchone()
            cursor.close()
            self.assertEqual(result[0], 1, "Query did not return expected result")
        finally:
            if db_connection:
                returnconnection(db_connection)
                
    def test_real_dict_cursor(self):
        db_connection = None
        try:
            db_connection = getconnection()
            cursor = db_connection.cursor(cursor_factory=RealDictCursor)
            cursor.execute("SELECT 1 as test_value")   
            result = cursor.fetchone()
            self.assertEqual(result['test_value'], 1, "RealDictCursor did not return expected result")
        finally:
            if db_connection:
                returnconnection(db_connection)
                
    def test_multiple_connections(self):
        """Test for multiple connections form the pool"""
        connections = []
        try:
            #Get multiple connections
            for _ in range(3):
                conn = getconnection()
                self.assertTrue(is_connection_valid(conn), f"Connection {_+1} is not valid") # type: ignore
                connections.append(conn)
                #Verify 3 diff connections
                connection_ids = [id(conn) for conn in connections]
                self.assertEqual(len(set(connection_ids)), 3, "Did not get unique connections")
        finally:
            #Return connections to pool
            for conn in connections:
                returnconnection           
    def test_connection_return(self):
        """Test connections are returned to the pool"""
        initial_free = len(connection_pool._pool)
        
        #Get and immediately return a connection
        db_connection = getconnection()
        returnconnection(db_connection)
        
        #Check that count is same as previous
        final_free = len(connection_pool._pool)
        self.assertEqual(final_free, initial_free, "Connection was not properly returned to pool")
        
    def test_connection_close(self):
        """Test that connections can be closed and removed from the pool"""
        # Get initial count
        initial_total = len(connection_pool._pool) + len(connection_pool._used)
    
        # Get a connection and close it
        db_connection = getconnection()
        returnconnection(db_connection, close=True)
        
        # Total should now be one less
        final_total = len(connection_pool._pool) + len(connection_pool._used)
        self.assertEqual(final_total, initial_total, - 1)
        
if __name__ == 'main':
    try:
        unittest.main()
    finally:
        #Close everything (all conns)
        connection_pool.closeall()
        print("All connections closed")
            
                
        
        
                