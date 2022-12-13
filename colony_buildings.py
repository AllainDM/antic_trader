class ColonyBuildings:
    def __init__(self):
        self.buildings = {
            'Плантация(Оливки)': 1000,
            'Рудник(Медь)': 1000,
            'Невол.рынок(Рабы)': 1000,
            'Угодье(Шкуры)': 1000,
            'Поля(Зерно)': 1000,
        }

    def cost(self, buildings):
        return self.buildings[buildings]


colonyBuildings = ColonyBuildings()
