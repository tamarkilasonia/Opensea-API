import psycopg2

from dotenv import load_dotenv
import os

import logging

# Load environment variables from the .env file
load_dotenv()

# Access the values like this
db_host__var = os.environ.get('DB_HOST')
db_port__var = os.environ.get('DB_PORT')
db_name__var = os.environ.get('DB_NAME')
db_user__var = os.environ.get('DB_USER')
db_pass__var = os.environ.get('DB_PASS')

class Database:

    logging.basicConfig(level=logging.ERROR)

    def __init__(self, db_name=db_name__var, user=db_user__var, password=db_pass__var, host=db_host__var, port=db_port__var):
        """Initialize connection to PostgreSQL"""
        self.connection = psycopg2.connect(
            dbname=db_name, user=user, password=password, host=host, port=port
        )
        self.cursor = self.connection.cursor()

    def execute(self, query, params=()):
        """Execute INSERT, UPDATE, DELETE queries"""
        try:
            self.cursor.execute(query, params)
            self.connection.commit()
        except Exception as e:
            logging.error(f"Database execution error: {e}")
            self.connection.rollback()

    def executemany(self, query, params_list):
        try:
            self.cursor.executemany(query, params_list)
            self.connection.commit()
        except psycopg2.Error as e:
            logging.error(f"Database error: {e}")
            self.connection.rollback()
            raise

    def fetch(self, query, params=()):
        """Fetch data from the database"""
        try:
            self.cursor.execute(query, params)
            results = self.cursor.fetchall()
            return results
        except Exception as e:
            logging.error(f"Database fetch error: {e}")
            return []

    def close(self):
        """Close the database connection"""
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()