import sqlite3
from sqlite3 import Error
import json
import os


class QueryManager:
    def __init__(self, connection):
        self.connection = connection
        self.cursor = connection.cursor()

    def execute_query(self, query):
        try:
            self.cursor.execute(query)
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            print(f"An database related error occurred: {e}")
            return None

    def get_distinct_options(self, table_name, column_name):
        result = self.execute_query(f'SELECT DISTINCT {column_name} FROM {table_name} '
                                    f'WHERE {column_name} IS NOT NULL')
        return [row[0] for row in result]

    def get_search_query(self, table, constraints, limit=25, offset=0):
        query = f"SELECT * FROM {table}"
        if constraints:
            query += " WHERE " + " AND ".join(constraints)
        # Use -1 to get all results
        if limit != -1:
            query += f" LIMIT {limit} OFFSET {offset}"

        data = self.execute_query(query)
        if not data:
            data = []
            headers = []
            count = 0
        else:
            headers = [column[0] for column in self.cursor.description]
            count_query = f"SELECT COUNT(*) FROM {table}"
            if constraints:
                count_query += " WHERE " + " AND ".join(constraints)
            count = self.execute_query(count_query)[0][0]

        self.connection.cursor().close()
        return [data, headers, count]
