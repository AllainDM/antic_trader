from resources import goods


class Cities:
    def __init__(self):
        # Создадим экземпляр класса ресурсов.
        # Пока для
        self.goods_price = goods.resources_price
        self.cities_name_list = [
            "Карфаген",
            "Сиракузы",
            "Афины",
            "Родос",
            "Александрия",
            "Тир"
        ]

    def cities_available(self):
        return self.cities_name_list


cities = Cities()
