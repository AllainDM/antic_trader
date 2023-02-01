import pickle
import json
from datetime import datetime

from dynasty import Dynasty
from colony_buildings import buildings
from resources import goods


class FirstWorld:
    def __init__(self, row_id, date_create="0:0:0", is_active=1):
        self.row_id = row_id  # Номер игры
        self.is_active = 1  # Не активная игра считается как завершенная
        self.year = -300
        self.turn = 1

        self.dynasty = {}  # Основной объект с династиями
        self.dynasty_list = []  # Массив стран, для перебора при обсчете хода
        self.player_list = []

        # Товары и производство
        # А зачем нам это надо?
        self.goods = goods
        self.buildings = buildings

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
            "goods": self.goods,
            "buildings": self.buildings,
            "all_logs": self.all_logs,
            "date_create": self.date_create,
        }
        # Пишем в pickle.
        with open(f"games/{self.row_id}/gameID_{self.row_id}.trader", 'wb') as f:
            pickle.dump(data, f, pickle.HIGHEST_PROTOCOL)

    def load_from_file(self, game_id):
        # Прочитаем из pickle весь файл
        with open(f"games/{game_id}/gameID_{game_id}.trader", 'rb') as f:
            data = pickle.load(f)
        # Присвоим параметры
        self.row_id = data["row_id"]
        self.year = data["year"]
        self.turn = data["turn"]
        self.dynasty = data["dynasty"]  # Тут переменная в виде названия Династии на английском
        self.dynasty_list = data["dynasty_list"]  # И тут переменная в виде названия Династии на английском.....
        self.player_list = data["player_list"]
        self.goods = data["goods"]
        self.buildings = data["buildings"]
        self.all_logs = data["all_logs"]
        self.date_create = data["date_create"]
        # Проверим на ошибку чтение только что записанных данных

    def create_dynasty(self, row_id, player_id, name, name_rus, gold):
        # , win_points, colony, goods
        # При создании династии передаем название, но можно передавать ид
        # Нужно ли передавать ссылку self при создании Dynasty ?
        self.dynasty[name] = Dynasty(self, row_id=row_id, player_id=player_id, name=name, name_rus=name_rus, gold=gold)
        self.dynasty_list.append(name)
        self.player_list.append(player_id)
        self.dynasty[name].save_to_file()
        # !!!!!!!!!! Еще нужно запустить у Династии функцию сохранения ее данных в файл
        # Создадим файл с записью хода игрока. Он должен быть пустым при каждом создании игры
        acts = []
        with open(f"games/{self.row_id}/acts/gameID_{self.row_id}_playerID_{player_id}.trader", 'wb') as f:
            pickle.dump(acts, f, pickle.HIGHEST_PROTOCOL)
        return self.dynasty[name]

    # Восстановить династии из файла. Нужно для обсчета хода. Восстанавливаем все классы и считаем ход
    def restore_dynasty(self, game_id, player_id):
        print(f"Восстанавливаем династию: {player_id}")
        self.dynasty[player_id] = Dynasty(self)
        print(self.dynasty[player_id])
        self.dynasty[player_id].load_from_file(game_id, player_id)


def check_readiness(game_id):  # Проверить все ли страны отправили ход
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


def calculate_turn(game_id):
    # Изначально запускается отдельная функция определяющая готовность хода игроков
    # Теперь восстановим все классы игры взяв параметры из pickle
    game = FirstWorld(game_id)  # Восстановим саму игру.
    game.load_from_file(game_id)  # Запустим метод считающий данные из файла.
    for player_id in game.player_list:
        # !!!!!!!!!!! Мы тут получаем ИД игрока, а надо бы ИД династии.
        # !!!!!!!!!!! Можно было бы это совместить, но что будет, если меняется игрок на династии(стране)....
        # !!!!!!!!!!! Хотя вроде все верно, мы же забираем из подписанного файла ИДшником игрока
        print(f"Пред восстанавливаем династию: {player_id}")
        game.restore_dynasty(game_id, player_id)
    # Теперь нужно запустить собственно саму обработку действий
    # В случае начала обсчета хода, необходимо почистить лог прошлого хода у стран.
    # Или еще лучше, сделать массив вообще со всеми логами.
    # Может сделать отдельный массив в котором просто будут храниться все логи.
    for dyns in game.dynasty:
        game.dynasty[dyns].result_logs_text = []
    # Так же почистим общий лог
    game.all_logs = []
    # Проверю вообще считается ли действия через ссылку
    # Пока по 5 действий
    for cont in range(5):
        for dynasty_name in game.dynasty:
            print(f"Проверка ссылки: {dynasty_name}")
            print(f"Проверка ссылки: {game.dynasty[dynasty_name]}")
            game.dynasty[dynasty_name].calc_act()
    # Пост обсчет хода
    for dynasty_name in game.dynasty:
        game.dynasty[dynasty_name].calc_end_turn()
    # Сохраним данные для стран
    for dynasty_name in game.dynasty:
        game.dynasty[dynasty_name].save_to_file()
    # Добавим 1 к номеру хода и года
    game.year += 1
    game.turn += 1
    game.save_to_file()
