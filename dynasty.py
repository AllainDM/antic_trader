class Dynasty:
    def __init__(self, row_id, player_id, name, name_rus, gold=1000):
        self.row_id = row_id
        self.player_id = player_id
        self.name = name
        self.name_rus = name_rus
        self.gold = gold

        # Общие стартовые условия
        self.win_points = 0
        # Возможно вместо объектов использовать массив, для упрощенного поиска...
        # Пока в колонии может производиться только один вид товара
        self.colony = {
            "colony_goods1": 0,
            "colony_goods2": 0,
            "colony_goods3": 0,
            "colony_goods4": 0,
            "colony_goods5": 0,
        }
        self.goods = {
            "goods1": 0,
            "goods2": 0,
            "goods3": 0,
            "goods4": 0,
            "goods5": 0,
        }

        self.acts = []  # Список действий
        # self.logs = []
        self.result_logs_text = []  # Список с текстом выполненных действий
        self.logs_text = []  # Список с текстом не выполненных действий

        self.end_turn = False  # Отправила ли страна заявку

        # self.world = world  # Не помню, но для чего то нужно передать ссылку

    def return_var(self):
        data = {
            "name_rus": self.name_rus,
            "end_turn": self.end_turn,  # Отправим игроку статус хода, чтоб он был в курсе
            "gold": self.gold,
            # Товары и колонии
            "colony_goods1": self.colony["colony_goods1"],
            "colony_goods2": self.colony["colony_goods2"],
            "colony_goods3": self.colony["colony_goods3"],
            "colony_goods4": self.colony["colony_goods4"],
            "colony_goods5": self.colony["colony_goods5"],
            "goods1": self.goods["goods1"],
            "goods2": self.goods["goods2"],
            "goods3": self.goods["goods3"],
            "goods4": self.goods["goods4"],
            "goods5": self.goods["goods5"],
        }
        return data

    def calc_act(self):  # Подсчет одного действия для династии
        # if len(self.acts) > 0:
        if self.acts:
            print(f"""до: {self.acts}""")
            print(f"""Выполнено действие {self.acts[0]}""")
            self.acts.pop(0)
            print(f"""после: {self.acts}""")

    # Подсчет каких либо параметров после обсчета действия игроков. Обязательно выполняется после действий
    def calc_end_turn(self):

        # Выставим False для параметра end_turn
        self.end_turn = False

