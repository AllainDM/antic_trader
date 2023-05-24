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

    # Потребление товаров городом. Влияет на цену.
    # Каждый ход город по умолчание потребляет 3 товара
    def consumption_of_goods(self):
        for res in self.resources_name_list:
            self.resources_list[res] -= 5
            if self.resources_list[res] < 0:
                self.resources_list[res] = 0
            print(f"Запасов ресурсов в городе: {self.resources_list[res]}")

    # Получить цену ресурса
    def price(self, resources):
        # print("Пробуем подсчитать стоимость в классе")
        # Расчитаем доп модификатор спроса на товар
        # Цена падает при наличии 3+ товаров в городе
        price = self.resources_price[resources] * self.resources_mod_price[resources]
        if self.resources_list[resources] > 5:
            # 10% за каждое превышение больше 5, макс штраф 80%
            penalty = 1 - (self.resources_list[resources] - 5) * 0.1
            if penalty < 0.2:
                penalty = 0.2
            price = price * penalty
        return price

    # Получить список ресурсов
    def resources_available(self):
        return self.resources_name_list


goods = Goods()
