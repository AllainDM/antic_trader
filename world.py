import pickle

from dynasty import Dynasty
from colony_buildings import buildings
from resources import goods
from cities import cities
from events import events
from FDataBase import FDataBase

# Попробуем импортировать main для доступа к БД
# Нельзя, получается цикл
import maindb


class FirstWorld:
    def __init__(self, row_id, date_create="0:0:0", is_active=1, the_end=0):
        self.row_id = row_id  # Номер игры
        self.is_active = 1  # Не активная игра считается как завершенная
        self.year = -300
        self.turn = 1

        self.need_win_points_for_win = 10
        self.winners = []
        self.winners_ID = []
        self.game_the_end = False

        self.dynasty = {}  # Основной объект с династиями
        self.dynasty_list = []  # Массив стран, для перебора при обсчете хода
        self.player_list = []

        # Товары и производство
        self.buildings = buildings
        self.buildings_name = buildings.buildings_name_list  # Список названий построек
        self.cities = cities
        self.cities_name = cities.cities_name_list  # Список названий городов

        # Товары
        self.goods = goods  # Ссылка на класс
        # Список имен ресурсов для отображения на фронте сразу возьмем из класса
        self.goods_name = goods.resources_name_list

        # Общий лог событий. Сюда будут записываться все выполненные действия всех "игроков"
        self.all_logs = []

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
            "all_logs": self.all_logs,
            "date_create": self.date_create,

            "winners": self.winners,
            "game_the_end": self.game_the_end,
        }
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
        self.all_logs = data["all_logs"]
        self.date_create = data["date_create"]

        # Список победителей и статус игры, при окончании победитель повторно не определяется
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

    # Восстановить династии из файла. Нужно для обсчета хода. Восстанавливаем все классы и считаем ход
    def restore_dynasty(self, game_id, player_id, dynasty_name):
        # print(f"Восстанавливаем династию: {player_id}")
        self.dynasty[dynasty_name] = Dynasty(self)
        # print(self.dynasty[player_id])
        self.dynasty[dynasty_name].load_from_file(game_id, player_id)


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
    print(f"Создание династии {game.dynasty_list[-1]}")
    # print(f"Создание династии {game.dynasty[name]}")
    print(f"Общее количество династий: {len(game.dynasty_list)}")
    print(f"Общее количество династий: {len(game.dynasty)}")
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
    # Запустим глобальные/локальные евенты
    global_event = events.global_event()
    if global_event:
        game.all_logs.append(global_event)
    print(f"Глобальный евент {global_event}")
    # Пока по 5 действий. Нужно разделить по фазам, и что-то сделать в неограниченном количестве.
    # 20 для первого теста
    for cont in range(20):
        for dynasty_name in game.dynasty:
            # print(f"Проверка ссылки: {dynasty_name}")
            # print(f"Проверка ссылки: {game.dynasty[dynasty_name]}")
            game.dynasty[dynasty_name].calc_act()
    # Пост обсчет хода
    # !!!!!!!!!!!!!!!! Было просто game.dynasty. Но считалось 2 раза. А с dynasty_list другой баг
    print(f"game.dynasty: {game.dynasty}")
    for dynasty_name in game.dynasty:
        print(f"Почему запускается два раза? dynasty_name {dynasty_name}")
        game.dynasty[dynasty_name].calc_end_turn()
    # Запустим определение победителя
    if not game.game_the_end:
        check_winners(game)
    # Сохраним данные для стран
    # Данные сохраняем после всех изменений касающихся игрока, фронт потом запрашивает данные уже из файла
    for dynasty_name in game.dynasty:
        game.dynasty[dynasty_name].save_to_file()
    # Проверить список победителей
    # Добавим 1 к номеру хода и года
    game.year += 1
    game.turn += 1
    game.save_to_file()


# Напишем отдельно функцию определяющую победителя и оканчивающую игру
def check_winners(game):
    # Сначала посчитаем победные очки для всех стран
    for dynasty_name in game.dynasty:
        print(f"dynasty[dynasty_name]: {game.dynasty[dynasty_name]}")
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
