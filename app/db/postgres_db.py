from app.common.singleton import Singleton
import psycopg2
from psycopg2.extras import RealDictCursor
from loguru import logger as log


class Db(Singleton):
    _table_pk = {"tasks": "issue_id"}
    _db = {}
    _conn = None

    def __init__(self):
        self._conn = self.create_connection()

    def create_connection(self):
        try:
            connection = psycopg2.connect(
                host="db",
                user="postgres",
                password="postgres",
                database="web_dev",
                port="5432"
            )
            connection.autocommit = True
        except Exception as ex:
            print("[INFO] Error while connecting to PostgreSQL", ex)
            return None
        log.success("Connection to DB success")
        return connection

    def close_connection(self):
        if not self._conn:
            return
        self._conn.close()
        log.success("Connection to DB is closed")

    def init_schema(self, tablename, pk):
        try:
            with self._conn.cursor() as cursor:
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS tasks (
                        issue_id BIGINT PRIMARY KEY,
                        name VARCHAR NOT NULL,
                        description VARCHAR NULL,
                        created_at TIMESTAMP NOT NULL
                    );""")
                log.success("Table 'tasks' created successfully")
        except Exception as ex:
            log.error("[INFO] Error while creating table:" + str(ex))

    def insert_data(self):
        try:
            with self._conn.cursor() as cursor:
                cursor.execute("""
                            INSERT INTO tasks (name, description)  VALUES ('task1', 'description1') ON CONFLICT (issue_id) DO NOTHING;
                            INSERT INTO tasks (name, description)  VALUES ('task2', 'description2') ON CONFLICT (issue_id) DO NOTHING;
                            INSERT INTO tasks (name, description)  VALUES ('task3', 'description3') ON CONFLICT (issue_id) DO NOTHING;
                            INSERT INTO tasks (name, description)  VALUES ('task4', 'description4') ON CONFLICT (issue_id) DO NOTHING;
                            INSERT INTO tasks (name, description)  VALUES ('task5', 'description5') ON CONFLICT (issue_id) DO NOTHING;
                            INSERT INTO tasks (name, description)  VALUES ('task6', 'description6') ON CONFLICT (issue_id) DO NOTHING;
                            INSERT INTO tasks (name, description)  VALUES ('task7', 'description7') ON CONFLICT (issue_id) DO NOTHING;
                            INSERT INTO tasks (name, description)  VALUES ('task8', 'description8') ON CONFLICT (issue_id) DO NOTHING;
                            INSERT INTO tasks (name, description)  VALUES ('task9', 'description9') ON CONFLICT (issue_id) DO NOTHING;
                        """)
                log.success("Data inserted successfully")

        except Exception as ex:
            log.error("[INFO] Error while creating table:" + str(ex))

    def get_pk(self, tablename):
        return self._table_pk[tablename]

    def find_by(self, tablename: str, field: str, val=None) -> list:
        try:
            with self._conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute("SELECT * FROM tasks WHERE %s = %s;", (field, val))
                rows = cursor.fetchall()
        except Exception as ex:
            log.error("[INFO] Error while fetching data" + str(ex))
        if not rows or len(rows) == 0:
            return []

        return [dict(r) for r in rows]

    def add(self, tablename, cls, row):
        try:
            with self._conn.cursor() as cursor:
                cursor.execute(
                    'INSERT INTO tasks (name, description) VALUES (%s, %s) RETURNING issue_id',
                    (row.name, row.description))
                id_of_new_row = cursor.fetchone()[0]
                log.success("Task created successfully")
        except Exception as ex:
            log.error("[INFO] Error creating task:" + str(ex))
        return {"issue_id": id_of_new_row}

    def get_all(self, tablename):
        try:
            with self._conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute("SELECT * FROM tasks LIMIT 100;")
                rows = cursor.fetchall()
        except Exception as ex:
            log.error("[INFO] Error while fetching data" + str(ex))
        return [dict(r) for r in rows]

    def get_one(self, tablename, _id):
        rows = []
        try:
            with self._conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute("SELECT * FROM tasks WHERE issue_id = %s;", (str(_id),))
                rows = cursor.fetchall()
        except Exception as ex:
            log.error("[INFO] Error while fetching data" + str(ex))
        if not rows or len(rows) == 0:
            return None

        return dict(rows[0])

    # (TABLE_NAME, dto.Issue, issue_id, issue)
    def update_one(self, tablename, cls, _id, row):
        res = self.get_one(tablename, _id)
        if not res:
            return False
        try:
            with self._conn.cursor() as cursor:
                cursor.execute(
                    'UPDATE tasks SET name = %s, description = %s WHERE issue_id = %s',
                    (row.name, row.description, _id))
                log.success("Task updated successfully")
        except Exception as ex:
            log.error("[INFO] Error updating task:" + str(ex))
        return self.get_one(tablename, _id)

    def delete_one(self, tablename, _id):
        res = self.get_one(tablename, _id)
        if not res:
            return False
        try:
            with self._conn.cursor() as cursor:
                cursor.execute(
                    'DELETE FROM tasks WHERE issue_id = %s;',
                    (_id,))
                log.success("Task deleted successfully")
        except Exception as ex:
            log.error("[INFO] Error creating task:" + str(ex))
            return False
        return True


db = Db()
