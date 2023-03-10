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

    def add_game(self, turn, year, players, is_active=1):
        try:
            # Пока без даты, надо модифицировать таблицу
            date_create = datetime.strftime(datetime.now(), "%d.%m.%Y %H:%M:%S")  # Дата: день, часы, минуты
            self.__cur.execute("INSERT INTO games (is_active, turn, year, players, date_create) "
                               "VALUES(%s, %s, %s, %s, %s)",
                               (is_active, turn, year, players, date_create))
            self.__db.commit()
            print(f"Добавилось? turn:{turn} year: {year} players: {players} "
                  f"date_create: {date_create}")
        except Exception as _ex:
            print("Ошибка добавления данных в БД", _ex)
            return False

        return True

    def delete_game(self, game_id):  # "Удаление" игры на самом деле просто делает ее не активной
        # Возможно будет смысл сделать и кнопку полного удаления
        # Просто возникла сложность при создании новой игры, если ни одной не создано
        # Типо игра получает ИД 1, а в БД используется порядковый номер
        try:
            self.__cur.execute(f"UPDATE games set is_active = 0 WHERE row_id = {game_id}")
            self.__db.commit()
            print(f"Игра сделалась НЕ активной?")
        except Exception as _ex:
            print("Ошибка обновления данных в БД", _ex)
            return False

        return True

    def end_game(self, game_id):  # Окончание игры, можно продолжать играть, победитель определен
        try:
            self.__cur.execute(f"UPDATE games set the_end = 1 WHERE row_id = {game_id}")
            self.__db.commit()
            print(f"Игра окончена")
        except Exception as _ex:
            print("Ошибка обновления данных в БД", _ex)
            return False

        return True

    def get_all_games(self):
        try:
            self.__cur.execute(f"SELECT * FROM games WHERE is_active = 1")
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

    # Обновить счетчик побед у игрока
    def update_wins(self, user_id):
        print("Функция обновления считчика побед попыталась запуститься")
        try:
            # self.__cur.execute(f"UPDATE games set is_active = 0 WHERE row_id = {game_id}")
            # self.__cur.execute(f"UPDATE users set wins = 1 WHERE row_id = {user_id}")
            self.__cur.execute(f"UPDATE users set wins = wins + 1 WHERE row_id = {user_id}")
            self.__db.commit()
            print(f"Победа засчиталась?")
        except Exception as _ex:
            print("Ошибка обновления данных в БД", _ex)
            return False

        return True

    def update_win_game(self, game_id):
        print("Функция обновления считчика побед попыталась запуститься")
        try:
            self.__cur.execute(f"UPDATE games set the_end = 1 WHERE row_id = {game_id}")
            self.__db.commit()
            print(f"Партия окончена?")
        except Exception as _ex:
            print("Ошибка обновления данных в БД", _ex)
            return False

        return True

    # Получить количество побед у игрока
    # Есть общая функция получения инфы про игроков get_all_users, оттуда возьмем количество побед
    # def get_wins(self, user_id):
    #     try:
    #         self.__cur.execute(f"SELECT wins FROM users WHERE row_id = {user_id} LIMIT 1")
    #         res = self.__cur.fetchone()
    #         if not res:
    #             print("User not found")
    #             return False
    #
    #         return res
    #     except Exception as _ex:
    #         print("Ошибка поиска пользователя в БД", _ex)
    #
    #     return False
