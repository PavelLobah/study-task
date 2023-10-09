import psycopg2

# Проблема импорта настроек
from settings import get_settings

settings = get_settings()


def connect():
    try:
        connection = psycopg2.connect(
            host=settings.host,  # settings.host
            user="postgres",
            password="lobah2319",
            database="localDB",
            port="5432"
        )
        with connection.cursor() as cursor:
            cursor.execute('SELECT version()')
            print(f"Server version:{cursor.fetchone()}")

    except Exception as _ex:
        print("[INFO] Error while working with PostgreSQL", _ex)
    finally:
        if connection:
            connection.close()
            print("[INFO] PostgreSQL connection closed")


def create_db():
    try:
        connection = psycopg2.connect(
            host="localhost",
            user="postgres",
            password="lobah2319",
            database="localDB",
            port="5432"
        )
        with connection.cursor() as cursor:
            cursor.execute("""
        create table tasks
        ( id bigint primary key ,
        name varchar not null,
        description varchar not null,
        created_at timestamp not null
        );
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
            print("Table Created successfully")

    except Exception as _ex:
        print("[INFO] Error while working with PostgreSQL", _ex)
    finally:
        if connection:
            connection.close()
            print("[INFO] PostgreSQL connection closed")

def get_all():
    try:
        connection = psycopg2.connect(
            host="localhost",
            user="postgres",
            password="lobah2319",
            database="localDB",
            port="5432"
        )
        with connection.cursor() as cursor:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM tasks")
            rows = cursor.fetchall()
            for data in rows:
                print(f"ID: {data[0]} NAME: {data[1]} DESCRIPTION: {data[2]} CREATED_AT: {data[3]}")


    except Exception as _ex:
        print("[INFO] Error while working with PostgreSQL", _ex)
    finally:
        if connection:
            connection.close()
            print("[INFO] PostgreSQL connection closed")   


def init_schema(self, tablename, pk):
    conn = psycopg2.connect(database="your_database", user="your_user", password="your_password", host="your_host", port="your_port")
    cursor = conn.cursor()
    
    # Создаем таблицу, если она не существует
    create_table_query = f'''
        CREATE TABLE IF NOT EXISTS {tablename} (
            {pk} SERIAL PRIMARY KEY
        )
    '''
    cursor.execute(create_table_query)
    
    # Закрываем соединение с базой данных
    conn.commit()
    cursor.close()
    conn.close()




# create_db()
get_all()
# def get_all(tablename):
#         if connect():
#             with connection.cursor() as cursor:
#             cursor.execute('SELECT * FROM tablename')
#             print(f"Server version:{cursor.fetchone()}")



