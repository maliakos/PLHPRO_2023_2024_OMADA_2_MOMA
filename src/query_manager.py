import sqlite3
from sqlite3 import Error
import json
import os


class QueryManager:
    def __init__(self, connection):
        self.connection = connection
        self.cursor = connection.cursor()

    def execute_query(self, query, params):
        try:
            self.cursor.execute(query, params)
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")
            return None

    def get_all(self, table_name, columns):

      if columns.length == 0:
            columns_str = '*'
      else:
            columns_str = ', '.join(columns)
      return self.execute_query(f'SELECT ? FROM {table_name}', columns)

    def get_distinct(self, table_name, column_name):
        result = self.execute_query(f'SELECT DISTINCT {column_name} FROM {table_name} '
                                    f'WHERE {column_name} IS NOT NULL', ())
        return [row[0] for row in result]

    def get_custom(self, query):
        return self.execute_query(query, None)
