import psycopg2
import config
from datetime import datetime


def create_tables():
    try:
        conn = psycopg2.connect(
            host=config.host,
            user=config.user,
            password=config.password,
            database=config.db_name
        )

        # with conn.cursor() as cursor:
        #     cursor.execute(

        #     )

        cursor = conn.cursor()

        # cursor.execute("DROP TABLE IF EXISTS message")
        # cursor.execute("DROP TABLE IF EXISTS feedback")
        # print("Таблица удалена")
        # conn.commit()

        cursor.execute(""
                       "CREATE TABLE IF NOT EXISTS feedback ("
                       "row_id serial PRIMARY KEY, "
                       "message text, "
                       "user_id int);"
                       )
        print(f"{datetime.now()}: Таблица feedback создана")

        conn.commit()

        cursor.execute(""
                       "CREATE TABLE IF NOT EXISTS users ("
                       "row_id serial PRIMARY KEY, "
                       "login text NOT NULL, "
                       "psw text NOT NULL, "
                       "name text, "
                       "admin int);"
                       )
        print(f"{datetime.now()}: Таблица user создана")

        conn.commit()

        # cursor.execute("SELECT * FROM message")

        cursor.close()
        conn.close()

    except Exception as _ex:
        print("[INFO] Error while working with postgresql", _ex)
        file = open("logs.txt", "a")
        file.write(f"{datetime.now()}: [INFO] Error while working with postgresql {_ex} \n")
        file.close()


