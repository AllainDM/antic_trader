# from colony_buildings import buildings
import os
import pickle
import redis

from resources import goods  # Импортируем уже созданный экземпляр класса
from colony_buildings import buildings  # Импортируем уже созданный экземпляр класса


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

        # Ресурсы(товары)
        self.goods = goods  # Ссылка нужна для получения цены товара. Ссылку не сохраняем с прочими данными
        self.goods_list = goods.resources_list  # Тут загрузим словарь с ресурсами, на старте все значения == 0
        # Список с именами ресурсов
        self.goods_name_list = goods.resources_name_list  # Вроде не нужно, загружается из класса World

        self.buildings_list = buildings.buildings_list  # Тут загрузим словарь с ресурсами, на старте все значения == 0
        # Список с именами ресурсов
        self.buildings_name_list = buildings.buildings_name_list  # Вроде не нужно, загружается из класса World
        self.buildings_available_list = buildings.buildings_available(self.name)

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

            # Ссылку на класс нет необходимости сохранять
            # "goods": self.goods,
            "goods_list": self.goods_list,  # Список(словарь) ресурсов
            "goods_name_list": self.goods_name_list,  # Все таки сохраняем названия, для вывода их на фронт
            "buildings_list": self.buildings_list,
            "buildings_name_list": self.buildings_name_list,
            # Список доступных для строительства построек
            # !!!!!!! Это нужно не сохранять, а каждый раз обновлять из класса, мало ли что изменилось
            # !!!!!!! Нет, не из класса, класс не меняется, надо сохранять каждый конец хода в файле
            "buildings_available_list": self.buildings_available_list,

            "acts": self.acts,
            "result_logs_text": self.result_logs_text,
            "end_turn": self.end_turn,
            "end_turn_know": self.end_turn_know,
        }
        # print(f"self.goods: {self.goods}")
        # Пишем в pickle.
        # Тут нужно отловить ошибку отсутствия файла
        try:
            with open(f"games/{self.game_id}/gameID_{self.game_id}_playerID_{self.player_id}.trader", 'wb') as f:
                pickle.dump(data, f, pickle.HIGHEST_PROTOCOL)
        except FileNotFoundError:
            print(f"Файл 'games/{self.game_id}/gameID_{self.game_id}_playerID_{self.player_id}.trader' не найден")
            return ""
        # print(f"Данные игрока: {self.player_id}, игры: {self.game_id} сохранены")
        # print(data)

    def load_from_file(self, game_id, player_id):
        # Тут нужно отловить ошибку отсутствия файла
        try:
            with open(f"games/{game_id}/gameID_{game_id}_playerID_{player_id}.trader", 'rb') as f:
                data = pickle.load(f)
                # print(f"Восстанавливаем династию: {data}")
        except FileNotFoundError:
            print(f"Файл 'games/{game_id}/gameID_{game_id}_playerID_{player_id}.trader' не найден")
            return ""
        self.row_id = data["row_id"]
        self.game_id = data["game_id"]
        self.player_id = data["player_id"]
        self.name = data["name"]
        self.name_rus = data["name_rus"]
        self.gold = data["gold"]
        self.win_points = data["win_points"]

        # self.goods = data["goods"]
        self.goods_list = data["goods_list"]  # Список(словарь) ресурсов и их количество
        self.goods_name_list = data["goods_name_list"]
        self.buildings_list = data["buildings_list"]
        self.buildings_name_list = data["buildings_name_list"]
        # Список доступных для строительства построек
        # !!!!!!! Это нужно не сохранять, а каждый раз обновлять из класса, мало ли что изменилось
        self.buildings_available_list = data["buildings_available_list"]

        self.acts = data["acts"]
        self.result_logs_text = data["result_logs_text"]
        self.end_turn = data["end_turn"]
        self.end_turn_know = data["end_turn_know"]
        # print(f"Данные династии {self.name_rus} восстановились")
        # print(f"self.colony_buildings: {self.colony_buildings}")

    def calc_act(self):  # Подсчет одного действия для династии
        # print(f"Считаем ход для династии: {self.name}")
        if self.acts:
            # 1 индекс это первое по списку действие, первый элемент в списке, оно выполняется и удаляется
            # 2 индекс это индекс с ИД действия, он под индексом 1, под 0 текстовое описание. Начиная с 2 аргументы
            # Передавать ли аргументы в функцию или вытаскивать их уже в самой функции. Попробуем по разному =>
            if self.acts[0][1] == 101:
                self.act_build_colony(self.acts[0][2])  # Тут передадим аргумент
                print(f"""Выполнено действие {self.acts[0]}""")
                self.acts.pop(0)
            elif self.acts[0][1] == 201:
                self.act_sell_goods(self.acts[0][2], self.acts[0][3], self.acts[0][4])  # И тут передадим аргумент
                print(f"""Выполнено действие {self.acts[0]}""")
                self.acts.pop(0)
            elif self.acts[0][1] == 202:  # Продать вообще весь товар, аргументов только город
                self.act_sell_all_goods(self.acts[0][2])  # И тут передадим аргумент
                print(f"""Выполнено действие {self.acts[0]}""")
                self.acts.pop(0)
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
    def act_build_colony(self, buildings_name):     # 101 id
        # !!!!!!! На будущее нужно сделать сверку, доступна ли это постройка для игрока
        # print(f"self.game.buildings.buildings_cost: {self.game.buildings.buildings_cost}")
        # Два раза buildings это: 1 = экземпляр класса с постройками, 2 = список построек уже в классе
        # Преобразуем строку с золотом в число
        # !!!!!!!! Нужно подумать, где на другом этапе это можно сделать
        # print(f"buildings_name: {buildings_name}")
        self.gold = int(self.gold)
        # print(f"self.game.buildings.buildings_cost[buildings_name]:
        # {self.game.buildings.buildings_cost[buildings_name]}")
        if self.gold >= self.game.buildings_price[buildings_name]:
            # print(buildings[buildings_index])
            self.buildings_list[buildings_name] += 1  # Добавим постройку Династии
            self.game.buildings_list[buildings_name] += 1  # И добавим к общему количеству в стране
            self.gold -= self.game.buildings_price[buildings_name]

            self.result_logs_text.append(f"Вы построили {buildings_name}")
            self.game.all_logs.append(f"{self.name_rus} построили  {buildings_name}")
            # print(self.game.buildings.buildings[buildings_index])

    def calc_win_points(self):
        self.win_points = round(self.gold / 1000)
        print(f"Победные очки {self.name_rus}: {self.win_points}")
        return self.win_points

    def act_sell_goods(self, city, trade_goods, num):     # 201 id
        # Преобразуем строку с золотом в число
        # !!!!!!!! Нужно подумать, где на другом этапе это можно сделать
        self.gold = int(self.gold)
        # Прогоним цикл от количества продаваемого товара
        num = int(num)
        if num == -1:
            print("Продаем весь выбранный товар")
            if self.goods_list[trade_goods]:
                # for i in self.goods_list[trade_goods]:
                for i in range(self.goods_list[trade_goods]):
                    # self.gold += goods.resources_price[trade_goods]
                    print("Попытка запустить функцию подсчета стоимости товара")
                    goods_current_price = self.game.calc_goods_cost(city, trade_goods)
                    self.gold += goods_current_price
                    self.goods_list[trade_goods] -= 1
                    self.result_logs_text.append(f"Вы продали {trade_goods} в {city} по {goods_current_price}")
                    self.game.all_logs.append(f"{self.name_rus} продали {trade_goods} в {city}")
                    # Тестово отправляем запуск подсчета цены
            else:
                self.result_logs_text.append(f"Вы не продали {trade_goods}, товара нет в наличии")
        elif num > 0:
            if self.goods_list[trade_goods]:
                for i in range(num):
                    # self.gold += goods.resources_price[trade_goods]
                    print("Попытка запустить функцию подсчета стоимости товара")
                    goods_current_price = self.game.calc_goods_cost(city, trade_goods)
                    self.gold += goods_current_price
                    self.goods_list[trade_goods] -= 1
                    self.result_logs_text.append(f"Вы продали {trade_goods} в {city} по {goods_current_price}")
                    self.game.all_logs.append(f"{self.name_rus} продали {trade_goods} в {city}")
            else:
                self.result_logs_text.append(f"Вы не продали {trade_goods}, товара нет в наличии")

        # for i in num:
        #     if self.goods_list[trade_goods]:
        #         print(f"Товар {trade_goods} есть в наличии")
        #         # Получим золото взяв цену из класса товара
        #         self.gold += goods.resources_price[trade_goods]
        #         self.goods_list[trade_goods] -= 1
        #         self.result_logs_text.append(f"Вы продали {trade_goods} в {city}")
        #         self.game.all_logs.append(f"{self.name_rus} продали {trade_goods} в {city}")
        #     else:
        #         self.result_logs_text.append(f"Вы не продали {trade_goods}, товара нет в наличии")

    def act_sell_all_goods(self, city):     # 202 id
        # Преобразуем строку с золотом в число
        # !!!!!!!! Нужно подумать, где на другом этапе это можно сделать
        self.gold = int(self.gold)
        print("Попытка продать весь товар")
        for goods1 in self.goods_list:
            self.gold += self.goods_list[goods1] * self.goods.resources_price[goods1]
            self.goods_list[goods1] = 0
            print(self.goods_list[goods1] * self.goods.resources_price[goods1])
            # !!!!!!!!!!!!!!! С логом баг, выдает всего по 1, надо проработать выше по условию
            self.result_logs_text.append(f"Вы продали {goods1} в {city}")
        # if self.goods_list[trade_goods]:
        #     print(f"Товар {trade_goods} есть в наличии")
        #     # Получим золото взяв цену из класса товара
        #     self.gold += goods.resources_price[trade_goods]
        #     self.goods_list[trade_goods] -= 1
        #     self.result_logs_text.append(f"Вы продали {trade_goods} в {city}")
        #     self.game.all_logs.append(f"{self.name_rus} продали {trade_goods} в {city}")
        # else:
        #     self.result_logs_text.append(f"Вы не продали {trade_goods}, товара нет в наличии")

    def prod_goods(self):
        # Переберем список с постройками. Просто прибавим к товару количество соответствующих построек
        # Сама функция запускается в конце обработки хода игрока
        for i in range(len(self.buildings_name_list)):
            goods_name = self.buildings_name_list[i]
            # !!!!!!!!! Добавить в лог факт получения ресурса
            if self.buildings_list[goods_name] > 0:
                self.result_logs_text.append(
                    f"Вы произвели {self.buildings_list[goods_name]} {buildings.buildings_output_goods[goods_name]}.")
            self.goods_list[buildings.buildings_output_goods[goods_name]] += self.buildings_list[goods_name]

    # Отмена действий. Вторым аргументом количество, все, последний или номер индекса(еще не реализованно)
    def cancel_act(self, what):
        if what == "all":
            self.acts = []
        elif what == "last":
            self.acts.pop(-1)


