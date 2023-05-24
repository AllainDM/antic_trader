from resources import goods
import resources


class Settlement:
    def __init__(self, game, name, name_rus):
        self.name = name
        self.name_rus = name_rus
        # Создадим экземпляр класса ресурсов.
        self.goods_in_city = resources.Goods()
        # print(f"Экземпляр класса товары: {self.goods_in_city }")

    def cities_available(self):
        pass


