# from colony_buildings import buildings
import os
import pickle
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
        # Тут нужно отловить ошибку отсутствия файла
        try:
            with open(f"games/{self.game_id}/gameID_{self.game_id}_playerID_{self.player_id}.trader", 'wb') as f:
                pickle.dump(data, f, pickle.HIGHEST_PROTOCOL)
        except FileNotFoundError:
            print(f"Файл 'games/{self.game_id}/gameID_{self.game_id}_playerID_{self.player_id}.trader' не найден")
            return ""
        print(f"Данные игрока: {self.player_id}, игры: {self.game_id} сохранены")
        print(data)

    def load_from_file(self, game_id, player_id):
        with open(f"games/{game_id}/gameID_{game_id}_playerID_{player_id}.trader", 'rb') as f:
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

        # Выставим False для параметра end_turn
        self.end_turn = False
        self.save_to_file()
        print(f"Функция обработки конца хода")

    # Неактуальный метод. Теперь запускается как функция получая аргументами ИД партии и страны.
    def act_build_colony(self, buildings_index):     # 101 id
        print(self.game.buildings.buildings)
        # Два раза buildings это: 1 = экземпляр класса с постройками, 2 = список построек уже в классе
        # Преобразуем строку с золотом в число
        # !!!!!!!! Нужно подумать, где на другом этапе это можно сделать
        self.gold = int(self.gold)
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


