import sqlite3

DB_ROOT_PATH = "spider/dataset/database"


class SQLiteExecutor:
    def __init__(self):
        self.connections = {}

    def _get_conn(self, database_name):
        if database_name not in self.connections:
            self.connections[database_name] = sqlite3.connect(f"{DB_ROOT_PATH}/{database_name}/{database_name}.sqlite")
        return self.connections[database_name]

    def execute(self, database_name, query):
        conn = self._get_conn(database_name)
        cursor = conn.cursor()
        cursor.execute(query)
        return cursor.fetchall()


sqlite_executor = SQLiteExecutor()
