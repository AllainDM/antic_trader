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
        # Словарь с модификаторами цен на товары, будет установлены различные по городам
        self.resources_mod_price = {
            'Оливки': 2.5,
            'Медь': 1,
            'Рабы': 2,
            'Шкуры': 1.5,
            'Зерно': 1,
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
        print("Пробуем подсчитать стоимость в классе")
        return self.resources_price[resources] * self.resources_mod_price[resources]

    # Получить список ресурсов
    def resources_available(self):
        return self.resources_name_list


goods = Goods()
