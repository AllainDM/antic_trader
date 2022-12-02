from flask import Flask
import psycopg2
import config


def connect_to_db():
    try:
        conn = psycopg2.connect(
            host=config.host,
            user=config.user,
            password=config.password,
            database=config.db_name
        )

        # with conn.cursor() as cursor:
        #     cursor.execute(
        #         "SELECT version();"
        #     )

        cursor = conn.cursor()

        # cursor.execute("DROP TABLE IF EXISTS message CASCADE")
        # cursor.execute("DROP TABLE IF EXISTS users")
        # print("Таблица удалена")
        # conn.commit()

        # cursor.execute("CREATE TABLE IF NOT EXISTS message (row_id serial PRIMARY KEY, message text);")
        # print("Таблица создана")
        # conn.commit()

        # cursor.execute("INSERT INTO message (message) VALUES (%s)", ('new message 2',))
        # print("Сообщение добавлено")
        # conn.commit()

        # cursor.execute("ALTER TABLE users ADD COLUMN admin int")
        # print("Столбец добавлен добавлено")
        # conn.commit()

        cursor.execute(""
                       "CREATE TABLE IF NOT EXISTS users ("
                       "row_id serial PRIMARY KEY, "
                       "login text NOT NULL, "
                       "psw text NOT NULL, "
                       "name text, "
                       "admin int); "
                       )
        conn.commit()

        # cursor.execute("UPDATE users "
        #                "set psw = 'pbkdf2:sha256:260000$gF4CAWU05ubYwtLH$fff2152fcfb8b9a61df3670837efc6e9e7dace"
        #                "36309ddbda733b002e0b4fe6a6' "
        #                "where row_id = 1",)
        # print("Сообщение добавлено")
        # conn.commit()

        # cursor.execute("UPDATE users "
        #                "set admin = '1' "
        #                "where row_id = 1",)
        # print("Сообщение добавлено")
        # conn.commit()

        # cursor.execute("DELETE from users where row_id = 4",)
        # print("Пользователь удален")
        # conn.commit()

        # cursor.execute("SELECT * FROM message")
        #
        # one_line = cursor.fetchone()
        # print(one_line)
        #
        # fetch_all = cursor.fetchall()
        # # print(fetch_all[0][0])
        # for record in fetch_all:
        #     print(record)

        # cursor.execute("CREATE TABLE IF NOT EXISTS message (row_id serial PRIMARY KEY, message text, user_id int);")
        # print("Таблица создана")
        # conn.commit()
        #
        # cursor.execute("INSERT INTO users (login, psw, name, admin) "
        #                "VALUES (%s, %s, %s, %s)",
        #                ('admin', 'pbkdf2:sha256:260000$gF4CAWU05ubYwtLH$fff2152fcfb8b9a61df3670837efc6e9e7dace'
        #                            '36309ddbda733b002e0b4fe6a6',
        #                 'Админ', 1))
        # print("Сообщение добавлено")
        # conn.commit()
        #
        # cursor.execute("INSERT INTO users (login, psw, name, admin) "
        #                "VALUES (%s, %s, %s, %s)",
        #                ('test1', 'pbkdf2:sha256:260000$gF4CAWU05ubYwtLH$fff2152fcfb8b9a61df3670837efc6e9e7dace'
        #                          '36309ddbda733b002e0b4fe6a6',
        #                 'Тестовый1', 0))
        # print("Сообщение добавлено")
        # conn.commit()
        #
        # cursor.execute("INSERT INTO users (login, psw, name, admin) "
        #                "VALUES (%s, %s, %s, %s)",
        #                ('test2', 'pbkdf2:sha256:260000$gF4CAWU05ubYwtLH$fff2152fcfb8b9a61df3670837efc6e9e7dace'
        #                          '36309ddbda733b002e0b4fe6a6',
        #                 'Тестовый2', 0))
        # print("Сообщение добавлено")
        # conn.commit()
        #
        cursor.execute("SELECT * FROM users")

        one_line = cursor.fetchall()
        print(one_line)

        cursor.close()
        conn.close()

    except Exception as _ex:
        print("[INFO] Error while working with PostgreSQL", _ex)


connect_to_db()
