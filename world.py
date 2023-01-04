from dynasty import Dynasty
from colony_buildings import buildings
from resources import goods


class FirstWorld:
    def __init__(self, row_id, date):
        self.row_id = row_id  # Номер игры
        self.year = -300
        self.turn = 1

        self.dynasty = {}  # Основной объект с династиями
        self.dynasty_list = []  # Массив стран, для перебора при обсчете хода

        # Товары и производство
        # А зачем нам это надо?
        self.goods = goods
        self.buildings = buildings

        # Общий лог событий. Сюда будут записываться все выполненные действия всех "игроков"
        self.all_logs = []

        self.date_create = date  # Дата создания партии

    def create_dynasty(self, row_id, player_id, name, name_rus, gold):
        # , win_points, colony, goods
        # При создании династии передаем название, но можно передавать ид
        # Нужно ли передавать ссылку self при создании Dynasty ?
        self.dynasty[name] = Dynasty(self, row_id=row_id, player_id=player_id, name=name, name_rus=name_rus, gold=gold)
        self.dynasty_list.append(name)
        return self.dynasty[name]

    def calculate_turn(self):
        # Если хоть одна из стран не закончила ход, то выходим из функции
        # На будущее сделать проверку по таймеру, когда будет введено ограничение по времени хода
        # Проверку можно сделать и при запуске самой функции
        for i in range(len(self.dynasty)):
            if not self.dynasty[self.dynasty_list[i]].end_turn:
                # Если хоть у одной страны ход не "отправлен" функция прекращает работу
                return
        # В случае начала обсчета хода, необходимо почистить лог прошлого хода у стран.
        # Или еще лучше, сделать массив вообще со всеми логами.
        # Лучше сделать отдельный массив в котором просто будут храниться все логи.
        for dyns in range(len(self.dynasty_list)):
            self.dynasty[self.dynasty_list[dyns]].result_logs_text = []
        # Перебираем все династии и делаем по одному действию
        # Пока по 5 действий
        for cont in range(5):
            for dyns in range(len(self.dynasty_list)):
                self.dynasty[self.dynasty_list[dyns]].calc_act()
        # Пост обсчет хода
        for dyns in range(len(self.dynasty_list)):
            self.dynasty[self.dynasty_list[dyns]].calc_end_turn()
        # !!! Переношу это в пост обсчет для династии
        # В конце обсчета выставим end_turn = False для династий
        # for i in range(len(self.dynasty)):
        #     self.dynasty[self.dynasty_list[i]].end_turn = False
        # Добавим 1 к номеру хода и года
        self.year += 1
        self.turn += 1
