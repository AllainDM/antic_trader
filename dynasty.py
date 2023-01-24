# from colony_buildings import buildings

import redis
import pickle


# Настройка Redis для хранения данных игроков
rediska = redis.StrictRedis(
    host='127.0.0.1',
    port=6379,
    # password='qwerty',
    charset="utf-8",
    decode_responses=True
)


class Dynasty:
    def __init__(self, game, row_id=0, player_id=0, name="default_name", name_rus="Страна", gold=0):
        self.row_id = row_id
        self.player_id = player_id
        self.name = name
        self.name_rus = name_rus
        self.gold = gold

        # Общие стартовые условия
        self.win_points = 0
        # Возможно вместо объектов использовать массив, для упрощенного поиска...
        # Пока в колонии может производиться только один вид товара
        self.goods = [0, 0, 0, 0, 0]
        self.colony_buildings = [0, 0, 0, 0, 0]

        self.acts = []  # Список действий
        # self.logs = []
        # self.acts_text = []  # Список с текстом не выполненных действий
        self.result_logs_text = []  # Список с текстом выполненных действий

        self.end_turn = False  # Отправила ли страна заявку
        self.end_turn_know = True  # Прочитал ли оповещение о новом ходе

        # Это должно быть не у страны, а отдельный столбец у игрока в БД
        # self.active_game = 0  # Id Активной игры. Надо что-то решить и убрать 0

        self.game = game  # Не помню, но для чего то нужно передать ссылку
        self.game_id = game.row_id  # Сохраним ИД игры, для создания правильной ссылки при необходимости
        # Но конечно же, можно было бы передать ее аргументом при создании династии

    def save_to_file(self):
        data = {
            "row_id": self.row_id,
            "game_id": self.game_id,
            "player_id": self.player_id,
            "name": self.name,
            "name_rus": self.name_rus,
            "gold": self.gold,
            "win_points": self.win_points,
            "goods": self.goods,
            "colony_buildings": self.colony_buildings,
            "acts": self.acts,
            "result_logs_text": self.result_logs_text,
            "end_turn": self.end_turn,
            "end_turn_know": self.end_turn_know,
        }
        # Пишем в pickle.
        with open(f"games/gameID_{self.game_id}_playerID_{self.player_id}.trader", 'wb') as f:
            pickle.dump(data, f, pickle.HIGHEST_PROTOCOL)
        print(f"Данные игрока: {self.player_id}, игры: {self.game_id} сохранены")
        print(data)

    def load_from_file(self, game_id, player_id):
        with open(f"games/gameID_{game_id}_playerID_{player_id}.trader", 'rb') as f:
            data = pickle.load(f)
            print(f"Восстанавливаем династию: {data}")
        self.row_id = data["row_id"]
        self.game_id = data["game_id"]
        self.player_id = data["player_id"]
        self.name = data["name"]
        self.name_rus = data["name_rus"]
        self.gold = data["gold"]
        self.win_points = data["win_points"]
        self.goods = data["goods"]
        self.colony_buildings = data["colony_buildings"]
        self.acts = data["acts"]
        self.result_logs_text = data["result_logs_text"]
        self.end_turn = data["end_turn"]
        self.end_turn_know = data["end_turn_know"]
        print(f"Данные династии {self.name_rus} восстановились")

    # Неактуально, все параметры страны теперь записываются в файл
    # Отдельно запускаемая функция для хранения данных в Редис.
    # !!!!!!!!!! Вопрос пишем сохранение заново или нужна опция обновить для Редис ????
    # def save_to_redis(self):
    #     # !!!!!!! Тут запишем странам по 9999 золото, чтобы понять, что функция работает
    #     # !!!! То что выше, неактуально. Все работало....
    #     rediska.set(f"gameID_{self.game.row_id}_playerID_{self.player_id}_{self.gold}", self.gold)
    #     rediska.set(f"gameID_{self.game.row_id}_playerID_{self.player_id}_{self.name}", self.name)  # {self.name}
    #     rediska.set(f"gameID_{self.game.row_id}_playerID_{self.player_id}_{self.name_rus}", self.name_rus)
    #
    # def take_var_from_redis(self):
    #     self.gold = rediska.get(f"gameID_{self.game.row_id}_playerID_{self.player_id}_{self.gold}")
    #     self.name = rediska.get(f"gameID_{self.game.row_id}_playerID_{self.player_id}_{self.name}")
    #     self.name_rus = rediska.get(f"gameID_{self.game.row_id}_playerID_{self.player_id}_{self.name_rus}")

    # Неактуальный метод. Теперь данные берутся напрямую из файла
    # def return_var(self):
    #     print("Почему эта функция запускается больше одного раза?")
        # # Извлекём ход(действия) из файла
        # with open(f"games/acts/gameID_{self.game.row_id}_playerID_{self.player_id}.trader", "rb") as f:
        #     acts = pickle.load(f)
        # data = {
        #     # "name_rus": self.name_rus,
        #     "name_rus": rediska.get(f'gameID_{self.game.row_id}_playerID_{self.player_id}_{self.name_rus}'),
        #     "end_turn": self.end_turn,  # Отправим игроку статус хода, чтоб он был в курсе
        #     # "gold": self.gold,
        #     "gold": rediska.get(f'gameID_{self.game.row_id}_playerID_{self.player_id}_{self.gold}'),
        #     # "acts": self.acts,
        #     # Возьмём список действий с документа
        #     "acts": acts,
        #     # "acts_text": self.acts_text,  # Список с текстом не выполненных действий
        #     "result_logs_text": self.result_logs_text,  # Список с текстом выполненных действий
        #     # Товары и колонии
        #     # Сделаем списком
        #     "goods": [
        #         self.goods[0],
        #         self.goods[1],
        #         self.goods[2],
        #         self.goods[3],
        #         self.goods[4],
        #     ],
        #     "colony_buildings": [
        #         self.colony_buildings[0],
        #         self.colony_buildings[1],
        #         self.colony_buildings[2],
        #         self.colony_buildings[3],
        #         self.colony_buildings[4],
        #     ],
        # }
        # return data

    def calc_act(self):  # Подсчет одного действия для династии
        # if len(self.acts) > 0:
        print(f"Считаем ход для династии: {self.name}")
        if self.acts:
            # 1 индекс это первое по списку действие, первый элемент в списке, оно выполняется и удаляется
            # 2 индекс это индекс с ИД действия, он под индексом 1, под 0 текстовое описание. Начиная с 2 аргументы
            # Передавать ли аргументы в функцию или вытаскивать их уже в самой функции. Попробуем по разному =>
            if self.acts[0][1] == 101:
                self.act_build_colony(self.acts[0][2])  # Тут передадим аргумент
                print(f"""Выполнено действие {self.acts[0]}""")
                self.acts.pop(0)
            elif self.acts[0][1] == 201:
                self.act_sell_goods()  # А тут не будем передавать аргумент
                print(f"""Выполнено действие {self.acts[0]}""")
                # print(f"""до: {self.acts}""")
                self.acts.pop(0)
                # print(f"""после: {self.acts}""")
            else:
                print('Записей в акте нет')

    # Подсчет каких либо параметров после обсчета действия игроков. Обязательно выполняется после действий
    # Типо какие-нибудь налоги или наоборот доп доход
    # Производство товаров будет обрабатываться здесь
    def calc_end_turn(self):
        self.prod_goods()  # Произведем товары в "колониях"

        # !!!!!!!!!! Нам не нужно чистить акты, они могут остаться на следующий ход
        # Очистим файл с ходом(актами)
        # self.acts = []  # !!!!!! Возможно без self, типо самостоятельная переменная
        # with open(f"games/acts/gameID_{self.game.row_id}_playerID_{self.player_id}.trader", "wb") as f:
        #     pickle.dump(self.acts, f, pickle.HIGHEST_PROTOCOL)

        # Выставим False для параметра end_turn
        self.end_turn = False
        self.save_to_file()
        print(f"Функция обработки конца хода")

    # Неактуальный метод. Теперь запускается как функция получая аргументами ИД партии и страны.
    def act_build_colony(self, buildings_index):     # 101 id
        print(self.game.buildings.buildings)
        # Два раза buildings это: 1 = экземпляр класса с постройками, 2 = список построек уже в классе
        # # Скачаем параметры из Редис. В данном случае нужно золото
        # self.take_var_from_redis()
        # Преобразуем строку с золотом в число
        # !!!!!!!! Нужно подумать, где на другом этапе это можно сделать
        self.gold = int(self.gold)
        if self.gold >= self.game.buildings.buildings[buildings_index][1]:  # Индекс 1 это цена у постройки
            # print(buildings[buildings_index])
            self.colony_buildings[buildings_index] += 1
            self.gold -= self.game.buildings.buildings[buildings_index][1]
            # # Сохраним новый результат в Редис. Пока только по золоту, но возможно и что-то еще.
            # # !!!!!!!!!!! Саму постройку например
            # self.save_to_redis()
            self.result_logs_text.append(f"Вы построили {self.game.buildings.buildings[buildings_index][0]}")
            self.game.all_logs.append(f"{self.name_rus} построили  {self.game.buildings.buildings[buildings_index][0]}")
            print(self.game.buildings.buildings[buildings_index])

    def act_sell_goods(self):     # 201 id
        pass

    def prod_goods(self):
        # Переберем список с постройками. Просто прибавим к товару количество соответствующих построек
        # Сама функция запускается в конце обработки хода игрока
        for i in range(len(self.colony_buildings)):
            self.goods[i] += self.colony_buildings[i]

    # Отмена действий. Вторым аргументом количество, все, последний или номер индекса(еще не реализованно)
    def cancel_act(self, what):
        if what == "all":
            self.acts = []
        elif what == "last":
            self.acts.pop(-1)


# def act_build_colony(player_id, game_id, buildings_index):     # 101 id
#     # print(self.game.buildings.buildings)
#     # # Два раза buildings это: 1 = экземпляр класса с постройками, 2 = список построек уже в классе
#     # Скачаем параметры из файла
#     with open(f"games/gameID_{game_id}_playerID_{player_id}.trader", 'rb') as f:
#         data = pickle.load(f)
