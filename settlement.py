from resources import goods


class Settlement:
    def __init__(self, name_rus):
        # Создадим экземпляр класса ресурсов.
        # Пока для записи цены
        self.goods_price = goods.resources_price
        self.name_rus = name_rus

    def cities_available(self):
        pass


# settlement = Settlement()
