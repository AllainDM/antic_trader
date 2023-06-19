# from colony_buildings import buildings
import os
import pickle
import redis

from resources import goods  # Импортируем уже созданный экземпляр класса
from colony_buildings import buildings  # Импортируем уже созданный экземпляр класса
import decision  # Импортируем решения, будет обращаться напрямую


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
        self.title = 0  # Стартовый ранг игрока. За каждый дается 1 победное очко
        self.body_points = 3  # Очки действий для игрока
        # Остаток очков действий, для цикла подсчета хода. Восстанавливается перед подсчетом хода взяв значение выше
        self.body_points_left = self.body_points

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

        # Решения
        self.title_price = 1000
        self.donate_sum = 0

        self.acts = []  # Список действий
        # self.logs = []
        # self.acts_text = []  # Список с текстом не выполненных действий
        self.result_logs_text = []  # Список с текстом выполненных действий
        self.result_logs_text_all_turns = []  # Список с текстом выполненных действий по всем ходам

        self.end_turn = False  # Отправила ли страна заявку
        self.end_turn_know = True  # Прочитал ли оповещение о новом ходе

        # Это должно быть не у страны, а отдельный столбец у игрока в БД
        # self.active_game = 0  # Id Активной игры. Надо что-то решить и убрать 0

        self.game = game
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
            "donate_sum": self.donate_sum,
            "title": self.title,
            "win_points": self.win_points,
            "body_points": self.body_points,
            # Ссылку на класс нет необходимости сохранять
            # "goods": self.goods,
            "goods_list": self.goods_list,  # Список(словарь) ресурсов
            "goods_name_list": self.goods_name_list,  # Все таки сохраняем названия, для вывода их на фронт
            "buildings_list": self.buildings_list,
            "buildings_name_list": self.buildings_name_list,
            # Список доступных для строительства построек
            # TODO !!!!!!! Это нужно не сохранять, а каждый раз обновлять из класса, мало ли что изменилось
            # TODO !!!!!!! Нет, не из класса, класс не меняется, надо сохранять каждый конец хода в файле
            "buildings_available_list": self.buildings_available_list,
            "acts": self.acts,
            "result_logs_text": self.result_logs_text,
            "result_logs_text_all_turns": self.result_logs_text_all_turns,
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
        self.donate_sum = data["donate_sum"]
        self.title = data["title"]
        self.win_points = data["win_points"]
        self.body_points = data["body_points"]

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
        self.result_logs_text_all_turns = data["result_logs_text_all_turns"]
        self.end_turn = data["end_turn"]
        self.end_turn_know = data["end_turn_know"]

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
            elif self.acts[0][1] == 301:  # Купить титул
                self.act_buy_title()  # Аргументов нет
                print(f"""Выполнено действие {self.acts[0]}""")
                self.acts.pop(0)
            elif self.acts[0][1] == 302:  # Купить титул
                self.act_make_donate(self.acts[0][2])  # Аргументом сумма пожертвования
                print(f"""Выполнено действие {self.acts[0]}""")
                self.acts.pop(0)
            else:
                print('Записей в акте нет')

    # Подсчет каких либо параметров после обсчета действия игроков. Обязательно выполняется после действий
    # Типо какие-нибудь налоги или наоборот доп доход
    # Производство товаров будет обрабатываться здесь
    def calc_end_turn(self):
        self.prod_goods()  # Произведем товары в "колониях"

        # Выставим False для параметра подтверждающего отправку хода и получение оповещения о новом ходе
        self.end_turn = False
        self.end_turn_know = False
        self.save_to_file()
        print(f"Функция обработки конца хода")

    # Неактуальный метод. Теперь запускается как функция получая аргументами ИД партии и страны.
    def act_build_colony(self, buildings_name):     # 101 id
        # !!!!!!! На будущее нужно сделать сверку, доступна ли это постройка для игрока
        # Два раза buildings это: 1 = экземпляр класса с постройками, 2 = список построек уже в классе
        # Преобразуем строку с золотом в число
        # !!!!!!!! Нужно подумать, где на другом этапе это можно сделать
        self.gold = int(self.gold)
        if self.gold >= self.game.buildings_price[buildings_name]:
            self.buildings_list[buildings_name] += 1  # Добавим постройку Династии
            self.game.buildings_list[buildings_name] += 1  # И добавим к общему количеству в стране
            self.gold -= self.game.buildings_price[buildings_name]

            self.result_logs_text.append(f"Вы построили {buildings_name}")
            self.result_logs_text_all_turns.append(f"Ход {self.game.turn}. Вы построили {buildings_name}")
            self.game.all_logs.append(f"{self.name_rus} построили {buildings_name}")
            self.game.all_logs_party.append(f"Ход {self.game.turn}. "
                                            f"{self.name_rus} построили {buildings_name}")
        else:
            self.result_logs_text.append(f"Вы НЕ построили {buildings_name}, не хватило денег.")

    def calc_win_points(self):
        # Возьмем по 1 очку за 3000
        win_points = round(self.gold / 3000)
        # Дополнительное 1 очко, от лидера пожертвований
        # Определим сравнением имени победителя в записи игры
        if self.game.donate_leader == self.name_rus:
            win_points += 1
        # Добавим за титул
        win_points += self.title
        self.win_points = win_points
        # print(f"Победные очки {self.name_rus}: {self.win_points}")
        return win_points

    def act_sell_goods(self, city, trade_goods, num):     # 201 id
        # Преобразуем строку с золотом в число
        # !!!!!!!! Нужно подумать, где на другом этапе это можно сделать
        self.gold = int(self.gold)
        num = int(num)
        sum_tg = 0  # Количество проданного, для лога
        money_sum_tg = 0  # Общая сумма полученной выручки, для лога
        # Прогоним цикл от количества продаваемого товара
        if num == -1:
            print("Продаем весь выбранный товар")
            if self.goods_list[trade_goods] > 0:
                for i in range(self.goods_list[trade_goods]):
                    # Рассчитаем стоимость товара перед продажей
                    goods_current_price = self.game.calc_goods_cost(city, trade_goods)
                    self.gold += goods_current_price  # Добавим золото игроку
                    money_sum_tg += goods_current_price  # Общая сумма выручки для лога
                    sum_tg += 1  # Количество проданного, для лога
                    self.goods_list[trade_goods] -= 1  # Уменьшим количество товара на складе на 1
                    # Увеличим количество товаров в городе на 1
                    self.game.settlements[city].goods_in_city.resources_list[trade_goods] += 1
            else:
                self.result_logs_text.append(f"Вы не продали {trade_goods}, товара нет в наличии")
        elif num > 0:
            if self.goods_list[trade_goods] > 0:  # !!!!!!!!! Возможно можно убрать эту проверку
                for i in range(num):
                    # Вторая проверка на случай запроса на продажу товара больше чем есть
                    # Ибо тут отдельный цикл
                    if self.goods_list[trade_goods] > 0:
                        # Рассчитаем стоимость товара перед продажей
                        goods_current_price = self.game.calc_goods_cost(city, trade_goods)
                        self.gold += goods_current_price  # Добавим золото игроку
                        money_sum_tg += goods_current_price  # Общая сумма выручки для лога
                        sum_tg += 1  # Количество проданного, для лога
                        self.goods_list[trade_goods] -= 1  # Уменьшим количество товара на складе на 1
                        # Увеличим количество товаров в городе на 1
                        self.game.settlements[city].goods_in_city.resources_list[trade_goods] += 1
            else:
                self.result_logs_text.append(f"Вы не продали {trade_goods}, товара нет в наличии")
        if sum_tg > 0:  # Если хоть что-то продали, пишем лог
            self.result_logs_text.append(f"Вы продали {sum_tg} {trade_goods} в {city} на сумму {money_sum_tg}")
            self.result_logs_text_all_turns.append(f"Ход {self.game.turn}. "
                                                   f"Вы продали {sum_tg} {trade_goods} в {city} на сумму {money_sum_tg}")
            self.game.all_logs.append(f"{self.name_rus} продают {trade_goods} в {city}")
            self.game.all_logs_party.append(f"Ход {self.game.turn}. "
                                            f"{self.name_rus} продают {trade_goods} в {city}")

    def act_sell_all_goods(self, city):     # 202 id
        # Преобразуем строку с золотом в число
        # !!!!!!!! Нужно подумать, где на другом этапе это можно сделать
        self.gold = int(self.gold)
        sum_tg = 0  # Количество проданного, для лога
        money_sum_tg = 0  # Общая сумма полученной выручки, для лога
        # Собираем цикл по типам товаров
        for goods_type in self.goods_name_list:
            # Если этот товар есть
            if self.goods_list[goods_type] > 0:  # !!!!!!!!! Возможно можно убрать эту проверку
                for i in range(self.goods_list[goods_type]):
                    # Рассчитаем стоимость товара перед продажей
                    goods_current_price = self.game.calc_goods_cost(city, goods_type)
                    self.gold += goods_current_price  # Добавим золото игроку
                    money_sum_tg += goods_current_price  # Общая сумма выручки для лога
                    sum_tg += 1  # Количество проданного, для лога
                    self.goods_list[goods_type] -= 1  # Уменьшим количество товара на складе на 1
                    # Увеличим количество товаров в городе на 1
                    self.game.settlements[city].goods_in_city.resources_list[goods_type] += 1
        if sum_tg > 0:  # Если хоть что-то продали, пишем лог
            # !!!!!!!!! Не считаем товар по типам, просто считаем общее количество
            self.result_logs_text.append(f"Вы продали {sum_tg} товара в {city} на сумму {money_sum_tg}")
            self.result_logs_text_all_turns.append(f"Ход {self.game.turn}. "
                                                   f"Вы продали {sum_tg} товара в {city} на сумму {money_sum_tg}")
            self.game.all_logs.append(f"{self.name_rus} распродаются в {city}")
            self.game.all_logs_party.append(f"Ход {self.game.turn}. "
                                            f"{self.name_rus} распродаются в {city}")

    def act_buy_title(self):     # 301 id
        # Преобразуем строку с золотом в число
        # !!!!!!!! Нужно подумать, где на другом этапе это можно сделать
        self.gold = int(self.gold)
        # Рассчитаем стоимость покупки титула. Взяв стоимость из класса.
        # Аргументами передает текущий уровень титула и общее количество купленных и игре титулов(берется из мира)
        title_price_now = decision.decision.buy_title(self.title, self.game.title_total_taken)
        # Если хватает золота и ранг еще не максимальный
        if self.gold >= title_price_now and self.title < decision.decision.max_title:
            self.gold -= title_price_now       # Вычтем стоимость
            self.title += 1     # Добавим титул игроку
            self.game.title_total_taken += 1  # Добавим к общему счетчику купленных титутов у всех игроков
            self.result_logs_text.append(f"Вы купили титул за {title_price_now}")
            self.result_logs_text_all_turns.append(f"Ход {self.game.turn}. Вы купили титул за {title_price_now}")
            self.game.all_logs.append(f"{self.name_rus} покупают титул")
            self.game.all_logs_party.append(f"Ход {self.game.turn}. "
                                            f"{self.name_rus} покупают титул")
        else:
            self.result_logs_text.append(f"Вы не купили титул")

    def act_make_donate(self, donate_sum):  # 302 id
        # Преобразуем строку с золотом в число
        # !!!!!!!! Нужно подумать, где на другом этапе это можно сделать
        self.gold = int(self.gold)
        if self.gold >= donate_sum:
            self.gold -= donate_sum
            self.donate_sum += donate_sum
            self.result_logs_text.append(f"Вы сделали пожертвование на {donate_sum} золота")
            self.result_logs_text_all_turns.append(f"Ход {self.game.turn}. "
                                                   f"Вы сделали пожертвование на {donate_sum} золота")
            self.game.all_logs.append(f"{self.name_rus} делает пожертвование")
            self.game.all_logs_party.append(f"Ход {self.game.turn}. "
                                            f"{self.name_rus} делает пожертвование")
        else:
            self.result_logs_text.append(f"Вы не сделали пожертвование")

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


