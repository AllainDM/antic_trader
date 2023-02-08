class Goods:
    def __init__(self):
        self.resources_price = {
            'Оливки': 100,
            'Медь': 100,
            'Рабы': 100,
            'Шкуры': 100,
            'Зерно': 100,
        }
        self.resources_list = {
            'Оливки': 0,
            'Медь': 0,
            'Рабы': 0,
            'Шкуры': 0,
            'Зерно': 0,
        }
        self.resources_name_list = [
            'Оливки',
            'Медь',
            'Рабы',
            'Шкуры',
            'Зерно',
        ]
        # self.resources_list = [
        #     ['Оливки', 0],
        #     ['Медь', 0],
        #     ['Рабы', 0],
        #     ['Шкуры', 0],
        #     ['Зерно', 0],
        # ]

    def price(self, resources):
        return self.resources_price[resources]

    def resources_available(self):
        return self.resources_name_list


goods = Goods()
