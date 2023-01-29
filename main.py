from datetime import datetime
import pickle
import json

from flask import Flask, render_template, request, flash, g, redirect, url_for, jsonify
import psycopg2
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import login_required, current_user, login_user, LoginManager, logout_user
import redis

import config
import world
from FDataBase import FDataBase
from world import FirstWorld
from UserLogin import UserLogin
from dynasty import Dynasty
# import postgreTables


Debug = True
SECRET_KEY = config.SECRET_KEY

app = Flask(__name__)
app.config.from_object(__name__)

login_manager = LoginManager(app)
login_manager.login_view = "login"
login_manager.login_message = "Необходимо авторизоваться"
login_manager.login_message_category = 'error'

# Настройка Redis для хранения глобальной переменной Game
rediska = redis.StrictRedis(
    host='127.0.0.1',
    port=6379,
    # password='qwerty',
    charset="utf-8",
    decode_responses=True
)

print(rediska)

menu = [{"name": "Авторизация", "url": "login"},
        # {"name": "Игра", "url": "game"},
        {"name": "Feedback", "url": "contact"}]

menu_auth = [{"name": "Профиль", "url": "profile"},
             {"name": "Игра", "url": "game"},
             {"name": "Выбор игры", "url": "choose-game"},
             {"name": "Игроки", "url": "players"},
             {"name": "Feedback", "url": "contact"}]

menu_admin = [{"name": "Профиль", "url": "profile"},
              {"name": "Игры", "url": "games"},
              {"name": "Создать игру", "url": "create-game"},
              {"name": "Игроки", "url": "players"},
              {"name": "Feedback", "url": "contact"}]


def get_db():
    if not hasattr(g, 'link_db'):
        g.link_db = connect_db()
        # print("Соединение не было создано")
    # print("Соединение не было создано и мы его создали")
    return g.link_db


@app.teardown_appcontext
def close_db(error):
    # Закрываем соединение с БД, если оно было установлено
    if hasattr(g, 'link_db'):
        g.link_db.close()


dbase = None
"""
Создадим глобальную переменную - game. 
А так надо разобраться как получать такую переменную при каждой созданной игре.
Это требуется для одновременного создания нескольких игр, пока не понятно как себя поведет движок
"""
# game = {0: FirstWorld(1)}
# game = {0: FirstWorld(1, "0:0:0")}
# Массив с АЙДишниками игр, нужен для поиска в словаре(выше), используя как ключ
# game_arr = []

# # Запускать для обнуления файла со списком ИД игр
# with open(f"games/list.trader", 'wb') as f:
#     game_arr = []
#     # Сериализация словаря data с использованием последней доступной версии протокола.
#     pickle.dump(game_arr, f, pickle.HIGHEST_PROTOCOL)


# Прочитаем файл со списком игр
try:
    with open(f"games/list.trader", "rb") as f:
        # global game_arr
        game_arr = pickle.load(f)
except FileNotFoundError:
    print(f"Файл 'games/list.trader' не найден")

# На данный момент сохранение идет в Редис. Планируется перенести в БД
# Сделаем глобально массив с активными играми игроков. Индексом будет ИД игрока
# Временно напихаем сюда нулей. Вообще длинная должна равняться количеству зарегистрированных игроков
# active_games = []


@app.before_request
def before_request():
    # Database connection, before query
    global dbase
    db = get_db()
    dbase = FDataBase(db)


@login_manager.user_loader
def load_user(user_id):
    print(f"Load user. ID: {user_id}")
    return UserLogin().fromDB(user_id, dbase)


def connect_db():
    connect = psycopg2.connect(
        host=config.host,
        user=config.user,
        password=config.password,
        database=config.db_name
    )
    return connect


@app.route("/")
@app.route("/main")
@login_required
def index():
    user_admin = current_user.get_admin()
    if user_admin == 1:
        print("this is admin")
        return render_template("index.html", title="Main", menu=menu_admin)
    return render_template('index.html',  title="Main", menu=menu_auth)


# Что это за функция??????????????
@app.route("/create-game")
@login_required
def admin_create_new_game():
    user_admin = current_user.get_admin()
    if user_admin == 1:
        print("this is admin2")
        return render_template("create-game.html", title="Main", menu=menu_admin)
    return render_template('index.html',  title="Main", menu=menu_auth)


@app.route("/game")
@login_required
def play():
    user_admin = current_user.get_admin()
    user_name = current_user.get_name()
    player = int(current_user.get_id())
    if user_admin == 1:
        # Интересно, что открывается game-admin.html, но путь в адресной строке висит как "game"
        return render_template("game-admin.html", title=user_name, menu=menu_admin)
    else:
        # Извлекем активную игру из Редиски
        active_game = rediska.get(f'playerID_{player}_active_gameID')
        if active_game == 0:
            return render_template("new-game.html", title=user_name, menu=menu_auth)
        else:
            return render_template("game.html", title=user_name, menu=menu_auth)


@app.route("/choose-game")  # !!!!!!! Тире или нижнее подчеркивание??? Фронт тоже править
@login_required
def choose_game_html():  # Делаю подпись html, чтоб разделить названия функций с просто запросом страницы
    user_admin = current_user.get_admin()
    user_name = current_user.get_name()
    if user_admin == 1:
        return render_template("choose-game.html", title=user_name, menu=menu_admin)
    else:
        return render_template("choose-game.html", title=user_name, menu=menu_auth)


@app.route("/games")  # !!!!!!! Тире или нижнее подчеркивание??? Фронт тоже править
@login_required
def all_games_html():  # Делаю подпись html, чтоб разделить названия функций с просто запросом страницы
    user_admin = current_user.get_admin()
    user_name = current_user.get_name()
    if user_admin == 1:
        return render_template("games.html", title=user_name, menu=menu_admin)
    else:
        return render_template("game.html", title=user_name, menu=menu_auth)


@app.route("/load_all_games")
@login_required
def load_all_games():  # Делаю подпись html, чтоб разделить названия функций с просто запросом страницы
    global game_arr
    # Прочитаем файл со списком игр
    try:
        with open(f"games/list.trader", "rb") as f:
            game_arr = pickle.load(f)
    except FileNotFoundError:
        print(f"Файл 'games/list.trader' не найден")
        return ""
    games_list = []  # Это список игр для отправки админу
    for game in game_arr:
        games_list.append(game)
    print(f"games_list {games_list}")
    return jsonify(games_list)


@app.route("/delete_game")  # Удалить игру
@login_required
def delete_game():
    user_admin = current_user.get_admin()
    game_id = int(request.args.get('id'))
    if user_admin == 1:
        try:
            with open(f"games/list.trader", "rb") as f:  # Скачаем списко игр
                games = pickle.load(f)
                games.remove(game_id)  # Удалим по значение(ид игры с фронта)
            with open(f"games/list.trader", 'wb') as new_f:  # Обновим файл
                pickle.dump(games, new_f, pickle.HIGHEST_PROTOCOL)
        except FileNotFoundError:
            print(f"Файл 'games/list.trader' не найден")
    return ""


@app.route("/load_all_my_game")
@login_required
def load_all_my_game():  # Делаю подпись html, чтоб разделить названия функций с просто запросом страницы
    global game_arr
    # Прочитаем файл со списком игр
    try:
        with open(f"games/list.trader", "rb") as f:
            game_arr = pickle.load(f)
            print(f"game_arr {game_arr}")
    except FileNotFoundError:
        print(f"Файл 'games/list.trader' не найден")
        return ""
    # global game_arr
    player = int(current_user.get_id())
    games_list = []  # Это список игр для отправки игроку для выбора
    # with open(f"games/gamesID_{game_arr[-1]}_list_players.trader", "rb") as f:
    #     dynasty_list = pickle.load(f)  # Тут список ИД игроков у выбранной партии
    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    # Пока используем уже проверенный способ найти ид игрока в созданной игры
    # Потом сменить на нормальный поиск
    # И пока не понятно нужный ли ИД возвращается
    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    # for my_g in game_arr:
    #     for i in game[my_g].dynasty_list:
    #         if player == game[my_g].dynasty[i].player_id:
    #             print(f"Найдена игра с ИД: {my_g}")
    #             games_list.append(my_g)
    # Версия с извлечением списка игроков из файла
    print(f"game_arr: {game_arr}")
    game_index = 0  # Индекс выбранной игры
    for my_g in game_arr:  # game_arr прочитан из файла глобально !!!!!! НЕТ !!!!!!!! глобально опять ошибка
        print(f"my_g {my_g}")
        # Тут должен быть перебор всех файлов с играми
        # !!!!!!!!! Возможно быстрее создать отдельный файл с играми игрока заранее...... а может нет
        try:
            with open(f"games/gameID_{game_arr[game_index]}_list_players.trader", "rb") as f:
                dynasty_list = pickle.load(f)  # Тут список ИД игроков в выбранной партии
                print(f"Тут должен быть отображен список игроков у партии(ид: {game_arr[game_index]}): {dynasty_list}")
        except FileNotFoundError:
            print(f"Файл 'games/gameID_{game_arr[game_index]}_list_players.trader' не найден")
            return ""
        for i in dynasty_list:
            if player == i:
                print(f"Найдена игра с ИД: {my_g}")
                games_list.append(my_g)
        game_index += 1
    return jsonify(games_list)


@app.route("/set_active_game")
@login_required
def set_active_games():
    game_id = request.args.get('id')
    # game_id = int(game_id)
    active_game = int(game_id)
    # global active_games
    player = int(current_user.get_id())
    user_name = current_user.get_name()
    # player подсвечивается, но работает, мне бы понять почему
    # Уже не подсвечивается, преобразовал переменную в Int
    # active_games[player] = int(game_id)
    # Теперь сохраняем в редиску, можно так и оставить, если будет норм работать
    rediska.set(f"playerID_{player}_active_gameID", active_game)
    print(f"Игрок {user_name} сделал активной игру номер: {active_game}")
    return ""


@app.route("/players")
@login_required
def players_html():  # Делаю подпись html, чтоб разделить названия функций с просто запросом страницы
    user_admin = current_user.get_admin()
    user_name = current_user.get_name()
    if user_admin == 1:
        return render_template("players.html", title=user_name, menu=menu_admin)
    else:
        return render_template("players.html", title=user_name, menu=menu_auth)


@app.route("/req_list_players")
@login_required
def req_list_players():
    # Поиск игрока по участию в игре. В БД у пользователей планируется запись со списком игр с участием этого игрока
    # Проверка или в тексте запроса к БД. Тут нужен доп аргумент в виде ИД игры
    # Или проверка тут, через цикл по списку каждого пользователя.
    # Подходящие уже тогда добавляются на отправки на фронт
    # who = request.args.get('who')
    list_users_to_front = []
    # try:  # Блок на случай отсутствия файла
    #     # Прочитаем весь список активных игр
    #     with open(f"games/list.trader", 'rb') as f_games:
    #         list_games = pickle.load(f_games)
    users = dbase.get_all_user()
    for user in users:
        # Возвращаем имя пользователя(не логин) и ИД пользователя(для админа)
        list_users_to_front.append([user[0], user[3]])
    return jsonify(list_users_to_front)
    # except FileNotFoundError:
    #     print(f"Файл 'games/list.trader' не найден")
    #     return ""


@app.route("/create_test_new_game")
@login_required
def create_test_new_game():
    # Создать вариант, где пользователь не админ, что перекидывало куда-нибудь в другое место
    global game_arr
    user_admin = current_user.get_admin()
    if user_admin == 1:
        print("this is admin3")
        # Прочитаем файл со списком игр
        try:
            with open(f"games/list.trader", "rb") as f:
                game_arr = pickle.load(f)
        except FileNotFoundError:
            print(f"Файл 'games/list.trader' не найден")
            return ""
        # Создадим игру, пока она одна, позже проработать возможность создания нескольких
        if len(game_arr) == 0:
            game_arr.append(1)
        else:
            game_arr.append(game_arr[-1]+1)  # +1 тут по умолчанию, 0 индекс уже есть, длинна массива 1
        date_now = datetime.strftime(datetime.now(), "%d.%m.%Y %H:%M:%S")  # Дата: день, часы, минуты
        # Добавим в Редис общие параметры
        # rediska.set(f"gameID_{game_arr[-1]}_date", date_now)  # Время создания партии
        # rediska.set(f"gameID_{game_arr[-1]}_turn", 1)  # Номер первого хода
        # rediska.set(f"gameID_{game_arr[-1]}_date", year)  # Стартовая дата

        # Обновим список ИД игр с помощью pickle
        with open(f"games/list.trader", 'wb') as f:
            pickle.dump(game_arr, f, pickle.HIGHEST_PROTOCOL)

        # print(f"Игра {game_arr[-1]} создана(Redis): {rediska.get(f'gameID_{game_arr[-1]}_date')}")
        print(f"Игра {game_arr[-1]} создана: {date_now}")
        print(f"ID новой игры: {game_arr[-1]}")
        create_game(game_arr[-1], date_now)  # Передаем дату, чтоб она не обновлялась при "восстановлении" класса игры

        # Старое. Возврат страницы, игра создавалась просто по ссылке
        # return render_template("game.html", title="Main", menu=menu_admin)
        return jsonify("Ответ от Python: Игра создалась")
    else:
        # return render_template("game.html", title="Main", menu=menu_auth)
        return ""


@app.route("/create_new_game")
@login_required
def create_new_game():
    # Создать вариант, где пользователь не админ, что перекидывало куда-нибудь в другое место
    global game_arr
    user_admin = current_user.get_admin()
    if user_admin == 1:
        print("this is admin3")
        # Прочитаем файл со списком игр
        try:
            with open(f"games/list.trader", "rb") as f:
                game_arr = pickle.load(f)
        except FileNotFoundError:
            print(f"Файл 'games/list.trader' не найден")
            return ""
        # Создадим игру, пока она одна, позже проработать возможность создания нескольких
        if len(game_arr) == 0:
            game_arr.append(1)
        else:
            game_arr.append(game_arr[-1]+1)  # +1 тут по умолчанию, 0 индекс уже есть, длинна массива 1
        date_now = datetime.strftime(datetime.now(), "%d.%m.%Y %H:%M:%S")  # Дата: день, часы, минуты

        # Обновим список ИД игр с помощью pickle
        with open(f"games/list.trader", 'wb') as f:
            pickle.dump(game_arr, f, pickle.HIGHEST_PROTOCOL)

        print(f"Игра {game_arr[-1]} создана: {date_now}")
        print(f"ID новой игры: {game_arr[-1]}")
        create_game(game_arr[-1], date_now)  # Передаем дату, чтоб она не обновлялась при "восстановлении" класса игры
        return jsonify("Ответ от Python: Игра создалась")
    else:
        return ""


def create_game(num, date_now):  # Num, то есть ИД игры сейчас ну нужно, ибо не создается словарь с играми
    # global game
    # game[num] = FirstWorld(game_arr[-1])
    # game[num].create_dynasty(1, 2, "Barkid", "Баркиды", 10000)
    # game[num].create_dynasty(2, 3, "Magonid", "Магониды", 12000)

    this_game = FirstWorld(game_arr[-1], date_now)
    this_game.create_dynasty(1, 2, "Barkid", "Баркиды", 10000)
    this_game.create_dynasty(2, 3, "Magonid", "Магониды", 12000)
    this_game.save_to_file()

    # Создадим список игроков для игры
    with open(f"games/gameID_{game_arr[-1]}_list_players.trader", 'wb') as f:
        # !!!!!!!!!!! Тут нам нужно как то передать список(ИД) всех назначенных игроков
        list_players = [2, 3]
        pickle.dump(list_players, f, pickle.HIGHEST_PROTOCOL)
    # Переведем в json, чтоб открывать проверять файл вручную
    # with open(f'games/gameID_{game_arr[-1]}_list_players.json', 'w') as outfile:
    #     # !!!!!!!!!!! Тут нам нужно как то передать список(ИД) всех назначенных игроков
    #     list_players = [2, 3]
    #     json.dump(list_players, outfile)

    # Так же присвоим одноименным переменным созданные династии
    print("Игра на двоих создана")
    # Barkid = game[num].dynasty['Barkid']
    # Запустим сохранение параметров в Редис. !!! Пока ИД игроков статичны
    # game[num].dynasty['Magonid'].save_to_redis()
    # game[num].dynasty['Barkid'].save_to_redis()
    # this_game.dynasty['Magonid'].save_to_redis()
    # this_game.dynasty['Barkid'].save_to_redis()
    # game[num].dynasty[3].save_to_redis()
    # Magonid = game[num].dynasty['Magonid']
    print(this_game.dynasty_list)


# !!!!!!!!!! Отменять надо у Активной игры
@app.route("/cancel_act")
def cancel_act():
    what = request.args.get('what')
    # response = dbase.read_router_comment(id_router)
    player = int(current_user.get_id())
    # Получим ИД партии !!!!!!!!!!!! Обязательно проверку
    game_id = request.args.get('gameId')
    try:  # Блок на случай отсутствия файла
        with open(f"games/gameID_{game_id}_playerID_{player}.trader", 'rb') as f:
            data = pickle.load(f)
            if what == "all":
                data["acts"] = []
            elif what == "last":
                data["acts"].pop(-1)
            with open(f"games/gameID_{game_id}_playerID_{player}.trader", 'wb') as new_f:
                pickle.dump(data, new_f, pickle.HIGHEST_PROTOCOL)
        return "ok"
    except FileNotFoundError:
        print(f"Файл 'games/gameID_{game_id}_playerID_{player}.trader' не найден")
        return ""
    # what = request.args.get('what')
    # # response = dbase.read_router_comment(id_router)
    # global game
    # player = int(current_user.get_id())
    # for i in game[0].dynasty_list:
    #     if player == game[0].dynasty[i].player_id:
    #         game[0].dynasty[i].cancel_act(what)
    # return "ok"


@app.route("/req_status_all_player", methods=["GET"])
@login_required
def req_status_all_player():
    # player = int(current_user.get_id())
    game_id = request.args.get('gameId')
    return_data = []
    try:
        with open(f"games/gameID_{game_id}.trader", 'rb') as f:
            data_players = pickle.load(f)
    except FileNotFoundError:
        print(f"Файл 'games/gameID_{game_id}.trader' не найден")
        return ""
    # print(f"data_players: {data_players}")
    for player_id in data_players["player_list"]:
        # print(f"player_id: {player_id}")
        try:
            with open(f"games/gameID_{game_id}_playerID_{player_id}.trader", 'rb') as f:
                data_one_player = pickle.load(f)
                one_player = {
                    "name_rus": data_one_player["name_rus"],
                    "gold": data_one_player["gold"],
                    "end_turn": data_one_player["end_turn"],
                }
                return_data.append(one_player)
        except FileNotFoundError:
            print(f"Файл 'games/gameID_{game_id}_playerID_{player_id}.trader' не найден")
            return ""
    return jsonify(return_data)


@app.route("/req_status_game_player", methods=["GET"])
@login_required
def req_status_game_player():
    # global game
    # global active_games
    # # Берём последнюю игру из найденных
    # if game is not None:
    #     player = int(current_user.get_id())
    #     for i in game[active_games[player]].dynasty_list:
    #         if player == game[active_games[player]].dynasty[i].player_id:
    #             print(f"Наша страна: {game[active_games[player]].dynasty[i].name_rus}")
    #             var_to_front = game[active_games[player]].dynasty[i].return_var()
    #             print(game[active_games[player]].dynasty[i].return_var())
    #             return jsonify(var_to_front)
    #     return ""
    player = int(current_user.get_id())
    game_id = rediska.get(f'playerID_{player}_active_gameID')
    # print(f"ИД игры при запросе статуса: {game_id}")
    # Выходит что нам не нужно обращаться к классу Династии запуская ее метод
    try:
        with open(f"games/gameID_{game_id}_playerID_{player}.trader", 'rb') as f:
            data = pickle.load(f)
    except FileNotFoundError:
        print(f"Файл 'games/gameID_{game_id}_playerID_{player}.trader' не найден")
        return ""
    # print(f"Параметры династии: {data}")
    return jsonify(data)


@app.route("/req_status_game", methods=["GET"])
@login_required
def req_status_game():
    # global active_games
    # player = int(current_user.get_id())
    # user_name = current_user.get_name()
    # # print(f'Тут должен быть ид игры: {active_games[player]}')
    # if game is not None:
    #     data = {
    #         "year": game[active_games[player]].year,
    #         "turn": game[active_games[player]].turn,
    #         "all_logs": game[active_games[player]].all_logs,
    #         "game_id": game[active_games[player]].row_id,
    #         # "date_create": game[active_games[player]].date_create,
    #         "date_create": rediska.get(f'gameID_{active_games[player]}_date'),
    #         # "date_create": rediska.get(f'game_id_1_date'),
    #         "user_name": user_name,
    #         # "year": game[game_arr[-1]].year,
    #         # "turn": game[game_arr[-1]].turn,
    #         # "all_logs": game[game_arr[-1]].all_logs,
    #     }
    #     print(game)
    #     return jsonify(data)
    # else:
    #     return ""
    player = int(current_user.get_id())
    user_name = current_user.get_name()
    game_id = rediska.get(f'playerID_{player}_active_gameID')
    # print(f"ИД игры при запросе статуса династии: {game_id}")
    # !!!!!!!!! Тут еще нужна проверка на существование самой партии
    try:
        with open(f"games/gameID_{game_id}.trader", 'rb') as f:
            world = pickle.load(f)
    except FileNotFoundError:
        print(f"Файл 'games/gameID_{game_id}.trader' не найден")
        return ""
    print(world)
    data = {
            "year": world["year"],
            "turn": world["turn"],
            "all_logs": world["all_logs"],
            "game_id": world["row_id"],
            "date_create": world["date_create"],
            "user_name": user_name,
        }
    return jsonify(data)


# !!!!!!!!!!!!! Запустить функцию подсчета хода
@app.route("/post_turn", methods=["POST"])
@login_required
def post_turn():
    global active_games  # Список. Остается глобальной переменной, загружается при загрузке файла
    if request.method == "POST":
        # print('Запрос с js')
        # Определим игрока, чтоб понять от кого получен ход и куда его записать
        player = int(current_user.get_id())
        # Получим ИД партии, ей будем присваивать ход !!!!!!!!!!!! после проверки
        # !!!!!!!!! Нужна проверка участвует ли игрок в этой игре!!!!!!!!!!!!!!!!!!!!!!!!!!
        game_id = request.args.get('gameID')
        # print(f"ИД партии которой передается ход: {game_id}")
        # Получаем список с действиями игрока
        # post = request.get_json()  # Нет необходимости, функция просто пдтверждает готовность
        # print(f"Ход от игрока {player}: {post}")
        # Прочитаем файл игрока
        try:
            with open(f"games/gameID_{game_id}_playerID_{player}.trader", 'rb') as f:
                data = pickle.load(f)
        except FileNotFoundError:
            print(f"Файл 'games/gameID_{game_id}_playerID_{player}.trader' не найден")
            return ""
        # print(f"Тут вот {data}")
        # Присвоим ход игроку
        data["end_turn"] = True
        # print(f"Тут вот {data}")
        # Снова запишем ход
        with open(f"games/gameID_{game_id}_playerID_{player}.trader", 'wb') as f:
            pickle.dump(data, f, pickle.HIGHEST_PROTOCOL)
        # print(f"Тут вот снова {data}")
        world.check_readiness(game_id)
    # Временно возвращаем пустую строку
    return ""
    # Старый вариант
    # if request.method == "POST":
    #     print('Запрос с js')
    #     # Тут нужно получить переменные с фронта
    #     # Определим принадлежность игры к игроку через цикл, пройдясь по параметру player_id
    #     # Сравним с ид игрока, если совпадает запрашиваем и отправляет параметры
    #     for i in game[active_games[player]].dynasty_list:
    #         if player == game[active_games[player]].dynasty[i].player_id:
    #             # Получаем список с действиями игрока
    #             post = request.get_json()
    #             print(post)
    #             # Присваиваем список действий игрока конкретному игроку
    #             game[active_games[player]].dynasty[i].acts = post
    #             # Меняем переменную отвечающую за готовность хода
    #             game[active_games[player]].dynasty[i].end_turn = True
    #     # Запускаем саму обработку хода, там будет доп проверка все ли игроки прислали ход
    #     game[active_games[player]].calculate_turn()
    # # Временно возвращаем пустую строку
    # return ""


@app.route("/post_act", methods=["POST"])
@login_required
def post_act():
    """
        Отдельная функция получения одного действия.
        Необходима для отображения актуального списка действий,
        который не будет пропадать и сбиваться при обновлении странички.
        Ход при этом не считается отправленным.
    """
    # global active_games # Как бы да, оно загружается глобально. Но тут передача ИД игры идет с фронта
    if request.method == "POST":
        # print('Запрос с js')
        # Определим игрока, чтоб понять от кого получен ход и куда его записать
        player = int(current_user.get_id())
        # Получим ИД партии, ей будем присваивать акт !!!!!!!!!!!! после проверки
        game_id = request.args.get('gameID')
        # !!!!!!!!! Нужна проверка участвует ли игрок в этой игре!!!!!!!!!!!!!!!!!!!!!!!!!!
        # print(f"ИД партии которой передается ход: {game_id}")
        # Получаем список с действиями игрока
        post = request.get_json()
        # print(f"Ход от игрока {player}: {post}")
        # Прочитаем файл игрока
        try:
            with open(f"games/gameID_{game_id}_playerID_{player}.trader", 'rb') as f:
                data = pickle.load(f)
        except FileNotFoundError:
            print(f"Файл 'games/gameID_{game_id}_playerID_{player}.trader' не найден")
            return ""
        # print(f"Тут вот {data}")
        # Присвоим ход игроку
        data["acts"] = post
        # print(f"Тут вот {data}")
        # Снова запишем ход
        with open(f"games/gameID_{game_id}_playerID_{player}.trader", 'wb') as f:
            pickle.dump(data, f, pickle.HIGHEST_PROTOCOL)
        # print(f"Тут вот снова {data}")
    # Временно возвращаем пустую строку
    return ""

    # Старый вариант
    # global active_games
    # if request.method == "POST":
    #     print('Запрос с js')
    #     # Тут нужно получить переменные с фронта
    #     # Определим игрока, чтоб понять от кого получен ход и куда его записать
    #     player = int(current_user.get_id())
    #     # Определим принадлежность игры к игроку через цикл, пройдясь по параметру player_id
    #     # Сравним с ид игрока, если совпадает запрашиваем и отправляет параметры
    #     for i in game[active_games[player]].dynasty_list:
    #         if player == game[active_games[player]].dynasty[i].player_id:
    #             # Получаем список с действиями игрока
    #             post = request.get_json()
    #             print(post)
    #             # Присваиваем список действий игрока конкретному игроку
    #             game[active_games[player]].dynasty[i].acts = post
    #             print(f"Длинна списка с действиями: {len(post)}")
    #             print(post[0])
    #             # Перезапишем файл полностью, ибо по факту получаем не один акт, а сразу все
    #             # !!!!!!! Еще нужно отловить ошибку, если папка не существует
    #             # !!!!!!! И само собой отлавливать ошибку при чтении, если файла не существует
    #             # !!!!!!!!!!!!!!!!!!!!!!
    #             # !!!!!!! Или можно всегда создавать файл автоматически при создании игры, пустым
    #             # Тут вариант с pickle
    #             with open(f"games/acts/gameID_{game[active_games[player]].row_id}_"
    #                       f"playerID_{game[active_games[player]].dynasty[i].player_id}.trader", 'wb') as f:
    #                 # Сериализация словаря data с использованием последней доступной версии протокола.
    #                 pickle.dump(post, f, pickle.HIGHEST_PROTOCOL)
    #             # Просто для теста возвращаем результат
    #             with open(f"games/acts/gameID_{game[active_games[player]].row_id}_"
    #                       f"playerID_{game[active_games[player]].dynasty[i].player_id}.trader", 'rb') as f:
    #                 data = pickle.load(f)
    #                 print(f"Pickle: {data}")
    # # Временно возвращаем пустую строку
    # return ""


@app.route("/contact", methods=["POST", "GET"])
@login_required
def contact():
    if request.method == "POST":
        # Feedback is available only to authorized users
        if len(request.form['message']) > 3:
            flash('Message sent', category="success")
            # Неправильна форма глагола send, sent прошедшее время в утвердительной форме
            user_id = int(current_user.get_id())  # Определим id Юзера
            user = current_user.get_name()  # Определим имя Юзера
            dbase.add_feedback(request.form['message'], user_id, user)
        else:
            flash('Error send. Message text must be longer than 3 characters.', category="error")
    user_admin = current_user.get_admin()
    if user_admin == 1:
        print("this is admin")
        return render_template("contact.html", title="Feedback", menu=menu_admin)
    return render_template('contact.html',  title="Feedback", menu=menu_auth)


@app.route("/login", methods=["POST", "GET"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('profile'))
        # return render_template('profile.html', title="Авторизация", menu=menu)
    if request.method == "POST":
        user = dbase.get_user_by_login(request.form['login'])
        if user and check_password_hash(user[2], request.form['psw']):
            user_login = UserLogin().create(user)
            login_user(user_login)
            print(f"Текущий пользователь:", current_user.get_id())
            return redirect(request.args.get("next") or url_for("profile"))
        flash("Wrong login/password", category="error")
        print("Ошибка авторизации")

    return render_template('login.html',  title="Авторизация", menu=menu)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Вы вышли из аккаунта", "success")
    return redirect(url_for('login'))


@app.route('/profile')
@login_required
def profile():
    user_admin = current_user.get_admin()
    if user_admin == 1:
        print("this is admin")
        return render_template("profile.html", title="Профиль", menu=menu_admin)
    return render_template("profile.html", title="Профиль", menu=menu_auth)


# Создадим игру при заргузке, чтоб было проще тестить
# def create_two_base_games():
#     date_now_gl = datetime.strftime(datetime.now(), "%d.%m.%Y %H:%M:%S")  # Дата: день, часы, минуты
#     game_arr.append(len(game_arr))  # +1 тут по умолчанию, 0 индекс уже есть, длинна массива 1
#     rediska.set(f"gameId_{game_arr[-1]}_date", date_now_gl)
#     create_game(game_arr[-1])
#
#     date_now_gl = datetime.strftime(datetime.now(), "%d.%m.%Y %H:%M:%S")  # Дата: день, часы, минуты
#     game_arr.append(len(game_arr))  # +1 тут по умолчанию, 0 индекс уже есть, длинна массива 1
#     rediska.set(f"gameId_{game_arr[-1]}_date", date_now_gl)
#     create_game(game_arr[-1])
#
#
# print(game_arr)

if __name__ == '__main__':
    app.run(debug=True)

