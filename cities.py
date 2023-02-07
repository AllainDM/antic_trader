class Cities:
    def __init__(self):
        # self.cities = {
        #     'Карфаген': 'Карфаген',
        #     'Сиракузы': 'Сиракузы',
        #     'Афины': 'Афины',
        #     'Родос': 'Родос',
        #     'Александрия': 'Александрия',
        #     'Тир': 'Тир',
        # }
        self.cities = [
            "Карфаген", "Сиракузы", "Афины", "Родос", "Александрия", "Тир"
        ]

    def cities_available(self):
        return self.cities


cities = Cities()
