# from datetime import datetime
# import psycopg2


class FDataBase:
    def __init__(self, db):
        self.__db = db
        self.__cur = db.cursor()

    def get_menu(self):
        pass

    def get_user(self, user_id):
        try:
            self.__cur.execute(f"SELECT * FROM users WHERE row_id = {user_id} LIMIT 1")
            res = self.__cur.fetchone()
            if not res:
                print("User not found")
                return False

            return res
        except Exception as _ex:
            print("Ошибка поиска пользователя в БД", _ex)

        return False

    # Добавить сообщение в фидбек
    def add_feedback(self, mess, user_id):
        try:
            # Пока без даты, надо модифицировать таблицу
            # date = datetime.strftime(datetime.now(), "%Y.%m.%d %H:%M")  # Дата регистрации, день, часы, минуты
            self.__cur.execute("INSERT INTO feedback (message, user_id) VALUES(%s, %s)", (mess, user_id))
            self.__db.commit()
            print("Добавилось?")
        except Exception as _ex:
            print("Ошибка добавления данных в БД", _ex)
            return False

        return True

    def get_user_by_login(self, login):
        try:
            self.__cur.execute(f"SELECT * FROM users WHERE login = '{login}' LIMIT 1")
            res = self.__cur.fetchone()
            if not res:
                print("User not found")
                return False
            print("Пользователь найден")
            return res

        except Exception as _ex:
            print("Ошибка поиска пользователя в БД", _ex)

        return False
