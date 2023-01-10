# from colony_buildings import buildings

import redis


# Настройка Redis для хранения данных игроков
rediska = redis.StrictRedis(
    host='127.0.0.1',
    port=6379,
    # password='qwerty',
    charset="utf-8",
    decode_responses=True
)


class Dynasty:
    def __init__(self, game, row_id=0, player_id=0, name="default_name", name_rus="Страна", gold=3000):
        self.row_id = row_id
        self.player_id = player_id
        self.name = name
        self.name_rus = name_rus
        self.gold = gold

        # Общие стартовые условия
        self.win_points = 0
        # Возможно вместо объектов использовать массив, для упрощенного поиска...
        # Пока в колонии может производиться только один вид товара
        # self.colony = {
        #     "colony_goods1": 0,
        #     "colony_goods2": 0,
        #     "colony_goods3": 0,
        #     "colony_goods4": 0,
        #     "colony_goods5": 0,
        # }
        # self.goods = {
        #     "goods1": 0,
        #     "goods2": 0,
        #     "goods3": 0,
        #     "goods4": 0,
        #     "goods5": 0,
        # }
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

    # Отдельно запускаемая функция для хранения данных в Редис.
    # !!!!!!!!!! Вопрос пишем сохранение заново или нужна опция обновить для Редис ????
    def save_to_redis(self):
        # !!!!!!! Тут запишем странам по 9999 золото, чтобы понять что функция работает
        rediska.set(f"gameID_{self.game.row_id}_playerID_{self.player_id}_{self.gold}", 9999)
        rediska.set(f"gameID_{self.game.row_id}_playerID_{self.player_id}_{self.name}", {self.name})
        rediska.set(f"gameID_{self.game.row_id}_playerID_{self.player_id}_{self.name_rus}", {self.name_rus})
        # rediska.set(f"gameID_{self.game.row_id}_playerID_{self.player_id}_{self.gold}, {num})
        # rediska.set(f"gameID_{self.game.row_id}_playerID_{self.player_id}_{var}", {num})
        # rediska.set(f"gameID_{self.game.row_id}_playerID_{self.player_id}_{var}", {num})
        # rediska.set(f"gameID_{self.game.row_id}_playerID_{self.player_id}_{var}", {num})
        # rediska.set(f"gameID_{self.game.row_id}_playerID_{self.player_id}_{var}", {num})

    def return_var(self):
        data = {
            # "name_rus": self.name_rus,
            "name_rus": rediska.get(f'gameID_{self.game.row_id}_playerID_{self.player_id}_{self.name_rus}'),
            "end_turn": self.end_turn,  # Отправим игроку статус хода, чтоб он был в курсе
            # "gold": self.gold,
            "gold": rediska.get(f'gameID_{self.game.row_id}_playerID_{self.player_id}_{self.gold}'),
            "acts": self.acts,
            # "acts_text": self.acts_text,  # Список с текстом не выполненных действий
            "result_logs_text": self.result_logs_text,  # Список с текстом выполненных действий
            # Товары и колонии
            # Сделаем списком
            "goods": [
                self.goods[0],
                self.goods[1],
                self.goods[2],
                self.goods[3],
                self.goods[4],
            ],
            "colony_buildings": [
                self.colony_buildings[0],
                self.colony_buildings[1],
                self.colony_buildings[2],
                self.colony_buildings[3],
                self.colony_buildings[4],
            ],
            # "colony_goods1": self.colony["colony_goods1"],
            # "colony_goods2": self.colony["colony_goods2"],
            # "colony_goods3": self.colony["colony_goods3"],
            # "colony_goods4": self.colony["colony_goods4"],
            # "colony_goods5": self.colony["colony_goods5"],
            # "goods1": self.goods["goods1"],
            # "goods2": self.goods["goods2"],
            # "goods3": self.goods["goods3"],
            # "goods4": self.goods["goods4"],
            # "goods5": self.goods["goods5"],
        }
        return data

    def calc_act(self):  # Подсчет одного действия для династии
        # if len(self.acts) > 0:
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
        # Выставим False для параметра end_turn
        self.end_turn = False

    def act_build_colony(self, buildings_index):     # 101 id
        print(self.game.buildings.buildings)
        # Два раза buildings это: 1 = экземпляр класса с постройками, 2 = список построек уже в классе
        if self.gold >= self.game.buildings.buildings[buildings_index][1]:  # Индекс 1 это цена у постройки
            # print(buildings[buildings_index])
            self.colony_buildings[buildings_index] += 1
            self.gold -= self.game.buildings.buildings[buildings_index][1]
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
