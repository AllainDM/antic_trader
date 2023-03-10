class Goods:
    def __init__(self):
        # Словарь с ценами ресурсов
        self.resources_price = {
            'Оливки': 200,
            'Медь': 200,
            'Рабы': 200,
            'Шкуры': 200,
            'Зерно': 200,
        }
        # Словарь с ресурсами, присваивается при создании игры, все значения по нулям
        self.resources_list = {
            'Оливки': 0,
            'Медь': 0,
            'Рабы': 0,
            'Шкуры': 0,
            'Зерно': 0,
        }
        # Просто список с названиями ресурсов
        self.resources_name_list = [
            'Оливки',
            'Медь',
            'Рабы',
            'Шкуры',
            'Зерно',
        ]

    # Получить цену ресурса
    def price(self, resources):
        return self.resources_price[resources]

    # Получить список ресурсов
    def resources_available(self):
        return self.resources_name_list


goods = Goods()
