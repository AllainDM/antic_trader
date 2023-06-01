
class Decision:
    def __init__(self):
        # Покупка титула
        self.title_price = 1000  # Базовая стоимость
        self.title_total_taken = 0  # Количество взятых, влияет на стоимость
        self.title_cost_mod_all = 0.1  # Модификатор повышения стоимости за каждый купленный титул игроками
        self.title_cost_mod_one = 1000  # Модификатор повышения стоимости за каждый взятый титул игроком
        self.max_title = 3  # Максимально возможный титул

    def buy_title(self, player_title):
        # Вернем итоговую стоимости титула
        return self.title_price + \
            self.title_total_taken * self.title_cost_mod_all + \
            player_title * self.title_cost_mod_one


