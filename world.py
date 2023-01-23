import pickle
import json
from datetime import datetime

from dynasty import Dynasty
from colony_buildings import buildings
from resources import goods


class FirstWorld:
    def __init__(self, row_id):
        self.row_id = row_id  # Номер игры
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

        self.date_create = datetime.strftime(datetime.now(), "%d.%m.%Y %H:%M:%S")  # Дата создания партии

    def save_to_file(self):
        data = {
            "row_id": self.row_id,
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
        with open(f"games/gameID_{self.row_id}.trader", 'wb') as f:
            pickle.dump(data, f, pickle.HIGHEST_PROTOCOL)
        # Сохраняем в Редис дату создания
        # rediska.set(f"gameId_{self.row_id}_date_create", self.date_create)
        # Проверим на ошибку чтение только что записанных данных
        # print(f"Проверяем запись чтение файла партии. Запись: {data}")
        # self.load_from_file(self.row_id)

    def load_from_file(self, game_id):
        # Прочитаем из pickle весь файл
        with open(f"games/gameID_{game_id}.trader", 'rb') as f:
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
        # Проверим на ошибку чтение только что записанных данных
        # print(f"Проверяем запись чтение файла партии. Чтение: {data}")

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
        with open(f"games/acts/gameID_{self.row_id}_playerID_{player_id}.trader", 'wb') as f:
            pickle.dump(acts, f, pickle.HIGHEST_PROTOCOL)
        return self.dynasty[name]

    # Восстановить династии из файла. Нужно для обсчета хода. Восстанавливаем все классы и считаем ход
    def restore_dynasty(self):
        for i in self.dynasty:
            print(f"Восстанавливаем династию: {i}")
            self.dynasty[i] = Dynasty(self)
            print(self.dynasty[i])
            self.dynasty[i] = Dynasty(self)

    # Старый метод до переноса данных в pickle
    # def calculate_turn(self):
    #     # Если хоть одна из стран не закончила ход, то выходим из функции
    #     # На будущее сделать проверку по таймеру, когда будет введено ограничение по времени хода
    #     # Проверку можно сделать и при запуске самой функции
    #     for i in range(len(self.dynasty)):
    #         if not self.dynasty[self.dynasty_list[i]].end_turn:
    #             # Если хоть у одной страны ход не "отправлен" функция прекращает работу
    #             return
    #     # В случае начала обсчета хода, необходимо почистить лог прошлого хода у стран.
    #     # Или еще лучше, сделать массив вообще со всеми логами.
    #     # Лучше сделать отдельный массив в котором просто будут храниться все логи.
    #     for dyns in range(len(self.dynasty_list)):
    #         self.dynasty[self.dynasty_list[dyns]].result_logs_text = []
    #     # Перебираем все династии и делаем по одному действию
    #     # Пока по 5 действий
    #     for cont in range(5):
    #         for dyns in range(len(self.dynasty_list)):
    #             self.dynasty[self.dynasty_list[dyns]].calc_act()
    #     # Пост обсчет хода
    #     for dyns in range(len(self.dynasty_list)):
    #         self.dynasty[self.dynasty_list[dyns]].calc_end_turn()
    #     # !!! Переношу это в пост обсчет для династии
    #     # В конце обсчета выставим end_turn = False для династий
    #     # for i in range(len(self.dynasty)):
    #     #     self.dynasty[self.dynasty_list[i]].end_turn = False
    #     # Добавим 1 к номеру хода и года
    #     self.year += 1
    #     self.turn += 1


def calculate_turn(game_id):
    # Сначала запускается отдельная функция определяющая готовность хода игроков
    # Теперь восстановим все классы игры взяв параметры из pickle
    game = FirstWorld(game_id)  # Восстановим саму игру.
    game.load_from_file(game_id)  # Запустим метод считающий данные из файла.

    game.restore_dynasty()


def check_readiness(game_id):  # Проверить все ли страны отправили ход
    with open(f"games/gameID_{game_id}.trader", 'rb') as f:
        data_main = pickle.load(f)
    # num_player = len(data_main["player_list"])
    # num_dynasty = len(data_main["dynasty_list"])
    # print(f"Всего игроков: {num_player}")
    # print(f"Всего династий: {num_dynasty}")
    for i in data_main["player_list"]:
        with open(f"games/gameID_{game_id}_playerID_{i}.trader", 'rb') as f:
            end_turn_reading = pickle.load(f)
            if not end_turn_reading["end_turn"]:
                print("Как минимум один из игроков еще не готов")
                print(f"Игрок: {i}")
                return
    print("Все игроки готовы")
    calculate_turn(game_id)
