import psycopg2

# Проблема импорта настроек
# from ..settings import get_settings

# settings = get_settings()
def connect(self):
    try:
        connection = psycopg2.connect(
            host="localhost",
            user="postgres",
            password="lobah2319",
            database="localDB",
            port="5432"
        )
        return connection
    except Exception as ex:
        print("[INFO] Error while connecting to PostgreSQL", ex)

def close_connection(connection):
    if not connection:
        return
    connection.close()
    print("[INFO] PostgreSQL connection closed")


def create_table():
    connection = connect()
    if not connection:
        return

    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS tasks (
                    id BIGINT PRIMARY KEY,
                    name VARCHAR NOT NULL,
                    description VARCHAR NOT NULL,
                    created_at TIMESTAMP NOT NULL
                )
            """)
            connection.commit()
            print("Table 'tasks' created successfully")
    except Exception as ex:
        print("[INFO] Error while creating table", ex)
    finally:
        close_connection(connection)


def insert_data():
    connection = connect()
    if not connection:
        return

    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                insert into tasks values (1, 'task1', 'description1', '2019-01-01 07:00:00');
                insert into tasks values (2, 'task2', 'description2', '2019-01-04 15:00:00');
                insert into tasks values (3, 'task3', 'description3', '2019-01-05 23:00:00');
                insert into tasks values (4, 'task4', 'description4', '2019-01-08 23:00:00');
                insert into tasks values (5, 'task5', 'description5', '2019-01-11 23:00:00');
                insert into tasks values (6, 'task6', 'description6', '2019-01-11 22:00:00');
                insert into tasks values (7, 'task7', 'description7', '2019-01-11 23:00:00');
                insert into tasks values (8, 'task8', 'description8', '2019-01-12 23:00:00');
                insert into tasks values (9, 'task9', 'description9', '2019-01-12 23:00:00');
            """)
            connection.commit()
            print("Data inserted successfully")

    except Exception as ex:
        print("[INFO] Error while creating table", ex)
    finally:
        close_connection(connection)


def get_all():
    connection = connect()
    if not connection:
        return

    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM tasks")
            rows = cursor.fetchall()
            for data in rows:
                print(
                    f"ID: {data[0]} NAME: {data[1]} DESCRIPTION: {data[2]} CREATED_AT: {data[3]}")
    except Exception as ex:
        print("[INFO] Error while fetching data", ex)
    finally:
        close_connection(connection)



# create_table()
# insert_data()
# get_all()


class Db:
    def connect(self):
        try:
            self.connection = psycopg2.connect(
                host="localhost",
                user="postgres",
                password="lobah2319",
                database="localDB",
                port="5432"
            )
            return self.connection
        except Exception as ex:
            print("[INFO] Error while connecting to PostgreSQL", ex)


    def __init__(self):
        self.conn = connect(self)
        self.cursor = self.conn.cursor()

    def init_schema(self, tablename, pk):
        create_table_query = f"CREATE TABLE IF NOT EXISTS {tablename} ({pk} SERIAL PRIMARY KEY);"
        self.cursor.execute(create_table_query)
        self.conn.commit()

    # def get_pk(self, tablename):
    #     return "id"  # Предполагается, что первичный ключ всегда называется "id"

    def find_by(self, tablename, field, val=None):
        if val is not None:
            select_query = f"SELECT * FROM {tablename} WHERE {field} = %s;"
            self.cursor.execute(select_query, (val,))
        else:
            select_query = f"SELECT * FROM {tablename} WHERE {field} IS NOT NULL;"
            self.cursor.execute(select_query)
        results = self.cursor.fetchall()
        return results, [result[0] for result in results]

    def add(self, tablename, cls, row):
        columns = []
        values = []
        for column, value in row.dict().items():
            columns.append(column)
            values.append(value)
        insert_query = f"INSERT INTO {tablename} ({','.join(columns)}) VALUES ({','.join(['%s'] * len(values))}) RETURNING *;"
        self.cursor.execute(insert_query, tuple(values))
        added_row = self.cursor.fetchone()
        obj = cls(**dict(zip(columns, added_row[1:])))
        self.conn.commit()
        return obj

    def get_all(self, tablename):
        select_query = f"SELECT * FROM {tablename};"
        self.cursor.execute(select_query)
        rows = self.cursor.fetchall()
        return rows

    def get_one(self, tablename, _id):
        select_query = f"SELECT * FROM {tablename} WHERE id = %s;"
        self.cursor.execute(select_query, (_id,))
        row = self.cursor.fetchone()
        if row:
            return row
        else:
            return None

    def update_one(self, tablename, cls, _id, row):
        columns = []
        values = []
        for column, value in row.dict().items():
            columns.append(column)
            values.append(value)
        update_query = f"UPDATE {tablename} SET {','.join([f'{c} = %s' for c in columns])} WHERE id = %s RETURNING *;"
        self.cursor.execute(update_query, tuple(values + [_id]))
        updated_row = self.cursor.fetchone()
        if updated_row:
            obj = cls(**dict(zip(columns, updated_row[1:])))
            self.conn.commit()
            return obj
        else:
            return None

    def delete_one(self, tablename, _id):
        delete_query = f"DELETE FROM {tablename} WHERE id = %s;"
        self.cursor.execute(delete_query, (_id,))
        num_deleted = self.cursor.rowcount
        self.conn.commit()
        return num_deleted > 0

    def close(connection):
        if not connection:
            return
        connection.close()
        print("[INFO] PostgreSQL connection closed")


db = Db()
