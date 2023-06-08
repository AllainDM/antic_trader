import pickle
from random import sample

from dynasty import Dynasty
from colony_buildings import buildings
from resources import goods
from cities import cities
from events import events
from FDataBase import FDataBase
from settlement import Settlement

# Попробуем импортировать main для доступа к БД
# Нельзя, получается цикл
import maindb


class FirstWorld:
    def __init__(self, row_id, date_create="0:0:0", is_active=1, the_end=0):
        self.row_id = row_id  # Номер игры
        self.is_active = 1  # Не активная игра считается как завершенная
        self.year = -300
        self.turn = 1

        self.need_win_points_for_win = 5
        self.winners = ""
        self.winners_ID = []
        self.game_the_end = False

        self.dynasty = {}  # Основной объект с династиями
        self.dynasty_list = []  # Массив стран, для перебора при обсчете хода
        self.player_list = []

        # Товары и производство
        self.buildings = buildings
        # Попробуем сохранить тут количество построек и их цену
        self.buildings_list = buildings.buildings_list
        # self.buildings_price = buildings.buildings_cost
        self.buildings_price = self.calc_buildings_cost()
        self.buildings_name = buildings.buildings_name_list  # Список названий построек

        # Решения
        self.donate_leader = "Не определен"  # Лидер по пожертвованиям, получает 1 победное очко
        # Сразу используем русское имя династии, с ним и сравниваем для определения победителя
        # self.donate_leader_name = "Не определен"  # Имя на русском для отправки на фронт
        # !!!!!! Пока не понятно нужно ли оно здесь, или будет храниться в классе(экземпляре)
        self.title_total_taken = 0  # Общее количество купленных титулов, влияет на стоимость

        # !!!!!!!!!! ЭТО НАДО????
        self.cities = cities
        self.cities_name = cities.cities_name_list  # Список названий городов

        # Создаем новый обьект с классом поселения
        self.settlements = {}
        self.settlements_list = []

        # Товары
        self.goods = goods  # Ссылка на класс
        # Список имен ресурсов для отображения на фронте сразу возьмем из класса
        self.goods_name = goods.resources_name_list
        # Словарь с городами и текущими ценами на товары. Рассчитываем отдельно в конце хода, для отправки на фронт
        self.all_goods_prices = self.calc_all_goods_price()

        # Общий лог событий. Сюда будут записываться все выполненные действия всех "игроков"
        self.all_logs = []
        self.all_logs_party = []  # Лог всей партии

        self.date_create = date_create

    def save_to_file(self):
        data = {
            "row_id": self.row_id,
            "is_active": self.is_active,
            "year": self.year,
            "turn": self.turn,
            "dynasty": self.dynasty,
            "dynasty_list": self.dynasty_list,
            "player_list": self.player_list,
            "donate_leader": self.donate_leader,
            "title_total_taken": self.title_total_taken,
            "buildings_price": self.calc_buildings_cost(),
            "buildings_list": self.buildings_list,
            "settlements": self.settlements,
            "settlements_list": self.settlements_list,
            "all_goods_prices": self.all_goods_prices,
            "all_logs": self.all_logs,
            "all_logs_party": self.all_logs_party,
            "date_create": self.date_create,

            "winners": self.winners,
            "need_win_points_for_win": self.need_win_points_for_win,
            "game_the_end": self.game_the_end,
        }
        print(f"save_to_file{data}")
        # Пишем в pickle.
        try:
            with open(f"games/{self.row_id}/gameID_{self.row_id}.trader", 'wb') as f:
                pickle.dump(data, f, pickle.HIGHEST_PROTOCOL)
        except FileNotFoundError:
            print(f"Файл 'games/{self.row_id}/gameID_{self.row_id}.trader' не найден")
            return ""

    def load_from_file(self, game_id):
        # Прочитаем из pickle весь файл
        try:
            with open(f"games/{game_id}/gameID_{game_id}.trader", 'rb') as f:
                data = pickle.load(f)
        except FileNotFoundError:
            print(f"Файл 'games/{game_id}/gameID_{game_id}.trader' не найден")
            return ""
        # Присвоим параметры
        self.row_id = data["row_id"]
        self.year = data["year"]
        self.turn = data["turn"]
        self.dynasty = data["dynasty"]  # Тут переменная в виде названия Династии на английском
        self.dynasty_list = data["dynasty_list"]  # И тут переменная в виде названия Династии на английском.....
        self.player_list = data["player_list"]
        self.donate_leader = data["donate_leader"]
        self.title_total_taken = data["title_total_taken"]
        self.buildings_price = data["buildings_price"]
        self.buildings_list = data["buildings_list"]
        self.settlements = data["settlements"]
        self.settlements_list = data["settlements_list"]
        self.all_goods_prices = data["all_goods_prices"]
        self.all_logs = data["all_logs"]
        self.all_logs_party = data["all_logs_party"]
        self.date_create = data["date_create"]

        # Список победителей и статус игры, при окончании победитель повторно не определяется
        self.need_win_points_for_win = data["need_win_points_for_win"]
        self.winners = data["winners"]
        self.game_the_end = data["game_the_end"]
        # Проверим на ошибку чтение только что записанных данных?????????

    def create_dynasty(self, row_id, player_id, name, name_rus, gold):
        # При создании династии передаем название, но можно передавать ид
        # Нужно ли передавать ссылку self при создании Dynasty ?
        self.dynasty[name] = Dynasty(self, row_id=row_id, player_id=player_id, name=name, name_rus=name_rus, gold=gold)
        self.dynasty_list.append(name)
        print(f"Создание династии {self.dynasty_list[-1]}")
        print(f"Создание династии {self.dynasty[name]}")
        print(self.dynasty[name])
        # print(f"Общее количество династий: {len(self.dynasty_list)}")
        # print(f"Общее количество династий: {len(self.dynasty)}")
        self.player_list.append(player_id)
        self.dynasty[name].save_to_file()
        # !!!!!!!!!! Еще нужно запустить у Династии функцию сохранения ее данных в файл
        # Создадим файл с записью хода игрока. Он должен быть пустым при каждом создании игры
        acts = []
        # !!!!!!!! Возможно тут повторная запись в файл, то же самое выполняем выше "self.dynasty[name].save_to_file()"
        # try:
        #     with open(f"games/{self.row_id}/acts/gameID_{self.row_id}_playerID_{player_id}.trader", 'wb') as f:
        #         pickle.dump(acts, f, pickle.HIGHEST_PROTOCOL)
        #     return self.dynasty[name]
        # except FileNotFoundError:
        #     print(f"Файл 'games/{self.row_id}/acts/gameID_{self.row_id}_playerID_{player_id}.trader' не найден")
        #     return ""

    # Создать поселение, тут на данный момент будет храниться проданный товар, излишек которого будет влиять на цену
    def create_settlement(self, name, name_rus):
        self.settlements[name] = Settlement(self, name=name, name_rus=name_rus)
        self.settlements_list.append(name)
        # print(self.settlements[name])

    # Восстановить династии из файла. Нужно для обсчета хода. Восстанавливаем все классы и считаем ход
    def restore_dynasty(self, game_id, player_id, dynasty_name):
        # print(f"Восстанавливаем династию: {player_id}")
        self.dynasty[dynasty_name] = Dynasty(self)
        # print(self.dynasty[player_id])
        self.dynasty[dynasty_name].load_from_file(game_id, player_id)

    # Рассчитаем стоимость построек, будет считаться в конце хода, в зависимости от количества и сохраняться в игру
    def calc_buildings_cost(self):
        sum_cost = {}
        b_list = self.buildings_list  # Возьмем словарь с количеством построек
        b_base_cost = self.buildings.buildings_cost  # Возьмем базовую цену построек из класса
        # Переберем словарь. Добавляем по 100 умноженное на количество
        for b in b_list:
            price = b_list[b] * 100 + b_base_cost[b]
            sum_cost[b] = price
        # print(f"Стоимость построек: {sum_cost}")
        # print(f"Количество построек: {b_list}")
        # print(f"Количество построек: {self.buildings_list}")
        return sum_cost

    # Рассчитаем стоимость всех товаров и обновим для мира. Нужно для отправки на фронт
    def calc_all_goods_price(self):
        goods_prices = {}
        for city in self.settlements:
            # Создадим переменную с названием страны
            print(f"city_4642 {city}")
            # print(f"city_5352 {self.settlements[city]}")
            nam = self.settlements[city].name
            # Запустим расчет цен по городам
            self.settlements[city].goods_in_city.price_all()
            # Присвоим городу словарь с текущими ценами
            goods_prices[nam] = self.settlements[city].goods_in_city.resources_curr_price
            # print(f"city_9836 {city}")
        # Вернем ответ, запрос идет для сохранения данных в мире
        print(f"Стоимость всех товаров расcчитана {goods_prices}")
        # Присвоим цены обьекту мира с ценами
        self.all_goods_prices = goods_prices
        return goods_prices

    # Рассчитаем стоимость товара для выбранного города, считаем отдельно на каждый товар
    def calc_goods_cost(self, city_gs, goods_to_sell):
        goods_sell_price = int(self.settlements[city_gs].goods_in_city.price(goods_to_sell))
        # print(f"Тут должна быть цена на {goods_to_sell}: {goods_sell_price}, в {city_gs}")
        return goods_sell_price

    def calc_donate_leader(self):
        donate_leader = ""
        donate_leader_sum = 0
        for i in self.dynasty:
            if self.dynasty[i].donate_sum > donate_leader_sum:
                donate_leader_sum = self.dynasty[i].donate_sum
                donate_leader = self.dynasty[i].name_rus
                self.donate_leader = self.dynasty[i].name_rus


def check_readiness(game_id):  # Проверить все ли страны отправили ход
    # Прочитаем общий файл с партией, нам понадобится список стран
    with open(f"games/{game_id}/gameID_{game_id}.trader", 'rb') as f:
        data_main = pickle.load(f)
    for i in data_main["player_list"]:
        with open(f"games/{game_id}/gameID_{game_id}_playerID_{i}.trader", 'rb') as f:
            end_turn_reading = pickle.load(f)
            if not end_turn_reading["end_turn"]:
                print("Как минимум один из игроков еще не готов")
                print(f"Игрок: {i}")
                return
    print("Все игроки готовы")
    calculate_turn(game_id)


# Функция должна запускаться при обсчете хода при восстановленных классах
# Функция определения победителя, проверяется в конце каждого хода
# def check_winner(game_id):
#     # Функция должна работать в рамках восстановленных классов стран???
#     # Прочитаем общий файл с партией, нам понадобится список стран
#     with open(f"games/{game_id}/gameID_{game_id}.trader", 'rb') as f:
#         data_main = pickle.load(f)
#     for i in data_main["player_list"]:
#         pass


def calculate_turn(game_id):
    # Изначально запускается отдельная функция определяющая готовность хода игроков
    # Теперь восстановим все классы игры взяв параметры из pickle
    game = FirstWorld(game_id)  # Восстановим саму игру.
    game.load_from_file(game_id)  # Запустим метод считающий данные из файла.
    # print(f"Создание династии {game.dynasty_list[-1]}")
    # print(f"Создание династии {game.dynasty[name]}")
    # print(f"Общее количество династий: {len(game.dynasty_list)}")
    # print(f"Общее количество династий: {len(game.dynasty)}")
    # Функция восстанавливая династию по списку игроков, присваивает экземпляр класса не к имени страны,
    # а к ИД игрока, от этого получается баг с клоном династии
    # for player_id in game.player_list:
    # !!!!!! Временно введем счетчик для соотношение ИД игрока от индекса страны с списке стран
    # !!!!!! По хорошему сделать что-то типо словаря, название строна: Ид игрока
    dynasty_playerID = 0
    for dynasty_name in game.dynasty_list:
        # !!!!!!!!!!! Мы тут получаем ИД игрока, а надо бы ИД династии.
        # !!!!!!!!!!! Можно было бы это совместить, но что будет, если меняется игрок на династии(стране)....
        # !!!!!!!!!!! Хотя вроде все верно, мы же забираем из подписанного файла ИДшником игрока
        # print(f"Пред восстанавливаем династию: {player_id}")
        game.restore_dynasty(game_id, game.player_list[dynasty_playerID], dynasty_name)
        dynasty_playerID += 1
    # Теперь нужно запустить собственно саму обработку действий
    # В случае начала обсчета хода, необходимо почистить лог прошлого хода у стран.
    # Или еще лучше, сделать массив вообще со всеми логами.
    # Может сделать отдельный массив в котором просто будут храниться все логи.
    for dyns in game.dynasty:
        game.dynasty[dyns].result_logs_text = []
    # Так же почистим общий лог
    game.all_logs = []
    # TODO отключил глобальные евенты
    # TODO Запустим глобальные/локальные евенты
    # TODO global_event = events.global_event()
    # TODO if global_event:
    # TODO     game.all_logs.append(global_event)
    # TODO     game.all_logs_party.append(f"Ход {game.turn}. {global_event}")
    # TODO print(f"Глобальный евент {global_event}")
    # Пробуем намутить по остаткам действий у стран
    # Введем переменную для цикла
    acts_left = True  # Будет проверяться в конце каждого цикла у игроков
    while acts_left:
    # for cont in range(20):
        # Отрандомим через random.sample список имен с династиями
        dyn_arr = sample(game.dynasty_list, len(game.dynasty_list))
        for rand_dynasty in dyn_arr:
        # for dynasty_name in game.dynasty:
            # Проверим остались ли очки действия у страны
            if game.dynasty[rand_dynasty].body_points_left > 0:
                acts_left = True  # Выставим верное значение, для продолжения обсчета цикла
                game.dynasty[rand_dynasty].calc_act()
                game.dynasty[rand_dynasty].body_points_left -= 1  # Вычтем действие после обсчета
            # Вычислим остались ли у игроков ходы
            else:
                acts_left = False   # Выставим ложь, если по итогу всего цикла ни у кого не осталось ходов

    # Пост обсчет хода
    # !!!!!!!!!!!!!!!! Было просто game.dynasty. Но считалось 2 раза. А с dynasty_list другой баг
    # print(f"game.dynasty: {game.dynasty}")
    for dynasty_name in game.dynasty:
        print(f"Почему запускается два раза? dynasty_name {dynasty_name}")
        game.dynasty[dynasty_name].calc_end_turn()
    # Рассчитаем лидера пожертвований
    game.calc_donate_leader()
    # Запустим определение победителя
    if not game.game_the_end:
        check_winners(game)
    # Обновим количество товаров в городе. Спишем за внутреннее потребление
    print("Обновим количество товаров в городе. Спишем за внутреннее потребление")
    for settlement in game.settlements_list:
        game.settlements[settlement].goods_in_city.consumption_of_goods()
    # После списания товаров обновим текущие цены, для возможности отдачи на фронт
    game.calc_all_goods_price()
    # Сохраним данные для стран
    # Данные сохраняем после всех изменений касающихся игрока, фронт потом запрашивает данные уже из файла
    for dynasty_name in game.dynasty:
        game.dynasty[dynasty_name].save_to_file()
    # Проверить список победителей
    # Добавим 1 к номеру хода и года
    game.year += 1
    game.turn += 1
    game.calc_buildings_cost()  # Обновим стоимость построек
    game.save_to_file()


# Напишем отдельно функцию определяющую победителя и оканчивающую игру
def check_winners(game):
    # Сначала посчитаем победные очки для всех стран
    for dynasty_name in game.dynasty:
        # print(f"dynasty[dynasty_name]: {game.dynasty[dynasty_name]}")
        # Посчитаем победные очки
        wp = game.dynasty[dynasty_name].calc_win_points()
        # Если их больше указанного количества записываем страну в список победителей
        if wp >= game.need_win_points_for_win:
            game.winners.append(game.dynasty[dynasty_name].name_rus)
            print(f"Ид победителя: {game.dynasty[dynasty_name].player_id}")
            game.winners_ID.append(game.dynasty[dynasty_name].player_id)
    print(f"winners: {game.winners}")
    # Если есть победители, надо их записать в БД
    # Необходимо определить страны победительницы, определить ИД игрока, и добавить в БД запись
    # Нужен цикл по массиву с победителями
    db = maindb.get_db()
    dbase = FDataBase(db)
    if len(game.winners_ID) > 0:
        for i in game.winners_ID:
            dbase.update_wins(i)
        # Сменим статус игры, заодно сохраним данные
        game.game_the_end = True
        game.save_to_file()
