from dynasty import Dynasty


class FirstWorld:
    def __init__(self, row_id):
        self.row_id = row_id  # Номер игры
        self.year = -300
        self.turn = 1

        self.dynasty = {}  # Основной объект с династиями
        self.dynasty_list = []  # Массив стран, для перебора при обсчете хода

    def create_dynasty(self, row_id, player_id, name, name_rus, gold):
        # , win_points, colony, goods
        # При создании династии передаем название, но можно передавать ид
        # Нужно ли передавать ссылку self при создании Dynasty ?
        self.dynasty[name] = Dynasty(row_id, player_id, name, name_rus, gold)
        self.dynasty_list.append(name)
        return self.dynasty[name]

    def calculate_turn(self):
        # Если хоть одна из стран не закончила ход, то выходим из функции
        # Проверку можно сделать и при запуске самой функции
        for i in range(len(self.dynasty)):
            if not self.dynasty[self.dynasty_list[i]].end_turn:
                return
        self.year += 1
        self.turn += 1
        # В конце обсчета выставим end_turn = False для династий
        for i in range(len(self.dynasty)):
            self.dynasty[self.dynasty_list[i]].end_turn = False
