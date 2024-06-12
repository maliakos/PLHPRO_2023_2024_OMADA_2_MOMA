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

    def get_max_min_dimensions_in_cm(self):
        query = ("SELECT ROUND(MIN(Height_cm),0) + 1  AS min_height, "
                 "ROUND(MAX(Height_cm),0) + 1 AS max_height, "
                 "ROUND(MIN(Width_cm),0) + 1 AS min_width, "
                 "ROUND(MAX(Width_cm),0) + 1 AS max_width "
                 "FROM Artworks "
                 "WHERE Height_cm  > 0 "
                 "AND Width_cm > 0")
        result = self.execute_query(query)
        return result[0]

    def get_search_query(self, table, constraints, limit=25, offset=0):
        query = f"SELECT * FROM {table}"
        if table == "Artworks":
            query += " LEFT JOIN Artists ON Artworks.ConstituentID = Artists.ConstituentID"

        if constraints:
            query += " WHERE " + " AND ".join(constraints)
        # Use -1 to get all results
        if limit != -1:
            query += f" LIMIT {limit} OFFSET {offset}"
        data = self.execute_query(query)
        print('main_query', query)
        if not data:
            data = []
            headers = []
            count = 0
        else:
            headers = [column[0] for column in self.cursor.description]
            count_query = f"SELECT COUNT(*) FROM {table}"
            if table == "Artworks":
                count_query += " LEFT JOIN Artists ON Artworks.ConstituentID = Artists.ConstituentID"
            if constraints:
                count_query += " WHERE " + " AND ".join(constraints)
            result = self.execute_query(count_query)
            if result is not None:
                count = result[0][0]
            else:
                count = 0

        self.connection.cursor().close()
        return [data, headers, count]
