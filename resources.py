class Goods:
    def __init__(self):
        self.resources = {
            'Оливки': 100,
            'Медь': 100,
            'Рабы': 100,
            'Шкуры': 100,
            'Зерно': 100,
        }

    def price(self, goods):
        return self.resources[goods]


goods = Goods()
