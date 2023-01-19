# # Извлекём ход(действия) из файла
#         with open(f"acts/gamesID_{self.game.row_id}_playerID_{self.player_id}.trader", "rb") as f:
#             acts = pickle.load(f)
#
#
#
#
# # Пишем
#                 with open(f"acts/gamesID_{game[active_games[player]].row_id}_"
#                           f"playerID_{game[active_games[player]].dynasty[i].player_id}.trader", 'wb') as f:
#                     # Сериализация словаря data с использованием последней доступной версии протокола.
#                     pickle.dump(post, f, pickle.HIGHEST_PROTOCOL)
#
#                 # Просто для теста возвращаем результат
#                 with open(f"acts/gamesID_{game[active_games[player]].row_id}_"
#                           f"playerID_{game[active_games[player]].dynasty[i].player_id}.trader", 'rb') as f:
#                     data = pickle.load(f)
#                     print(f"Pickle: {data}")
#
# Пишем экземпляр класса Мира(партии)
#         with open(f"games/gameID_{self.row_id}.trader", 'wb') as f:
#             pickle.dump(data, f, pickle.HIGHEST_PROTOCOL)
# Читаем
#         with open(f"games/gameID_{self.row_id}.trader", 'rb') as f:
#             data = pickle.load(f)

# Пишем экземпляр класса Династии(страны)
#         with open(f"games/gameID_{self.row_id}_playerID_{self.player_id}.trader", 'wb') as f:
#             pickle.dump(data, f, pickle.HIGHEST_PROTOCOL)
# Читаем
#         with open(f"games/gameID_{self.row_id}_playerID_{self.player_id}.trader", 'rb') as f:
#             data = pickle.load(f)