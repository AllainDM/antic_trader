import random

from resources import goods


class Events:
    def __init__(self):
        self.events_global_name_list = [
            "Падение спроса",
            "Рост спроса",
        ]
        self.events_local_name_list = [
            "Падение спроса",
            "Рост спроса",
            "Засуха",
            "Землетрясение",
            "Мятеж",
            "Набег варваров",
        ]

    def global_event(self):
        num_event = random.randint(0, 1)
        event = self.events_global_name_list[num_event]
        event_text = ""
        if event == "Падение спроса" or "Рост спроса":
            num_arg = random.randint(0, len(goods.resources_name_list) - 1)
            print(f"num_arg {num_arg}")
            print(f"num_arg {goods.resources_name_list[num_arg]}")
            event_text = f"{event} на {goods.resources_name_list[num_arg]}"
        return event_text


events = Events()
