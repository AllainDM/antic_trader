from datetime import datetime
# import psycopg2


class FDataBase:
    def __init__(self, db):
        self.__db = db
        self.__cur = db.cursor()

    def get_menu(self):
        pass

    def get_all_user(self):  # На будущее надо как то передавать ИД игры в которой участвует игрок.
        try:
            self.__cur.execute(f"SELECT * FROM users")
            res = self.__cur.fetchall()
            if not res:
                print("Users not found")
                return False

            return res
        except Exception as _ex:
            print("Ошибка поиска пользователей в БД", _ex)

        return False

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
    def add_feedback(self, mess, user_id, user_name):
        try:
            # Пока без даты, надо модифицировать таблицу
            date = datetime.strftime(datetime.now(), "%d.%m.%Y %H:%M")  # Дата: день, часы, минуты
            self.__cur.execute("INSERT INTO feedback (message, user_id, user_name, date) VALUES(%s, %s, %s, %s)",
                               (mess, user_id, user_name, date))
            self.__db.commit()
            print(f"Добавилось? id:{user_id} name: {user_name} text: {mess} date: {date}")
        except Exception as _ex:
            print("Ошибка добавления данных в БД", _ex)
            return False

        return True

    def add_game(self, turn, year, players):
        try:
            # Пока без даты, надо модифицировать таблицу
            date_create = datetime.strftime(datetime.now(), "%d.%m.%Y %H:%M:%S")  # Дата: день, часы, минуты
            self.__cur.execute("INSERT INTO games (turn, year, players, date_create) "
                               "VALUES(%s, %s, %s, %s)",
                               (turn, year, players, date_create))
            self.__db.commit()
            print(f"Добавилось? turn:{turn} year: {year} players: {players} "
                  f"date_create: {date_create}")
        except Exception as _ex:
            print("Ошибка добавления данных в БД", _ex)
            return False

        return True

    def delete_game(self, game_id):
        try:
            self.__cur.execute(f"DELETE FROM games WHERE row_id = {game_id}")
            self.__db.commit()
            print(f"Удалилось?")
        except Exception as _ex:
            print("Ошибка удаления данных из БД", _ex)
            return False

        return True

    def get_all_games(self):
        try:
            self.__cur.execute(f"SELECT * FROM games")
            res = self.__cur.fetchall()
            if not res:
                print("games not found")
                return []  # Вернем пустой список, для возможности добавления в него первого элемента

            return res
        except Exception as _ex:
            print("Ошибка поиска игр в БД", _ex)

        return False

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
