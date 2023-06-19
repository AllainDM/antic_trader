from datetime import datetime
import pickle
import json
import os

from flask import Flask, render_template, request, flash, g, redirect, url_for, jsonify
import psycopg2
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import login_required, current_user, login_user, LoginManager, logout_user
import redis

import maindb
import config
import world
from FDataBase import FDataBase
from world import FirstWorld
from UserLogin import UserLogin
from cities import Cities
from resources import Goods
from colony_buildings import ColonyBuildings
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
        {"name": "Feedback", "url": "contact"}]

menu_auth = [
             {"name": "Профиль", "url": "profile"},
             {"name": "Игра", "url": "game"},
             {"name": "Выбор игры", "url": "choose-game"},
             {"name": "Игроки", "url": "players"},
             {"name": "Лог", "url": "log"},
             # {"name": "Feedback", "url": "contact"}
]

menu_admin = [
              {"name": "Профиль", "url": "profile"},
              {"name": "Игры", "url": "games"},
              {"name": "Создать игру", "url": "create-game"},
              {"name": "Игроки", "url": "players"},
              {"name": "Лог", "url": "log"},
              # {"name": "Feedback", "url": "contact"}
]


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

# Массив с АЙДишниками игр
game_arr = []


@app.before_request
def before_request():
    # Database connection, before query
    global dbase
    db = maindb.get_db()
    dbase = FDataBase(db)


@login_manager.user_loader
def load_user(user_id):
    # print(f"Load user. ID: {user_id}")
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


@app.route("/game")  # Функция перенаправляет игрока на страницу смой игры, откуда уже происходит запрос параметров
@login_required
def play():
    user_admin = current_user.get_admin()
    user_name = current_user.get_name()
    player = int(current_user.get_id())
    if user_admin == 1:
        # Интересно, что открывается game-admin.html, но путь в адресной строке висит как "game"
        return render_template("game-admin.html", title=user_name, menu=menu_admin)
    else:
        # Извлекаем активную игру из Редиски
        # active_game = rediska.get(f'playerID_{player}_active_gameID')
        my_game_arr = dbase.get_all_games()
        if len(my_game_arr) == 0:
            return render_template("choose-game.html", title=user_name, menu=menu_auth)
        # if active_game == 0:
        #     return render_template("new-game.html", title=user_name, menu=menu_auth)
        else:
            return render_template("game.html", title=user_name, menu=menu_auth)


@app.route("/choose-game")  # Перенаправление на страничку выбора "активно" игры
@login_required
def choose_game_html():  # Делаю подпись html, чтоб разделить названия функций с просто запросом страницы
    user_admin = current_user.get_admin()
    user_name = current_user.get_name()
    if user_admin == 1:
        return render_template("choose-game.html", title=user_name, menu=menu_admin)
    else:
        return render_template("choose-game.html", title=user_name, menu=menu_auth)


@app.route("/games")  # Перенаправление на страничку со списком всех игр. ТОЛЬКО ДЛЯ АДМИНА
@login_required
def all_games_html():  # Делаю подпись html, чтоб разделить названия функций с просто запросом страницы
    user_admin = current_user.get_admin()
    user_name = current_user.get_name()
    if user_admin == 1:
        return render_template("games.html", title=user_name, menu=menu_admin)
    else:
        return render_template("game.html", title=user_name, menu=menu_auth)


# Страничка с логом изменений, а так же планом
@app.route("/log")
@login_required
def log():
    user_admin = current_user.get_admin()
    if user_admin == 1:
        print("this is admin")
        return render_template("log.html", title="Main", menu=menu_admin)
    return render_template('log.html',  title="Main", menu=menu_auth)


@app.route("/load_all_games")  # Посмотреть список все игр с возможностью их удаления. ТОЛЬКО ДЛЯ АДМИНА
@login_required
def load_all_games():  # Делаю подпись html, чтоб разделить названия функций с просто запросом страницы
    global game_arr
    # Прочитаем файл со списком игр
    game_arr = dbase.get_all_games()
    # Выше мы получили кортеж с данными страны, под 5 индексом список ИД игроков
    # Нужно перебрать список ИД игроков и вынести имена игроков
    print(f"game_arr: {game_arr}")
    games_list = []  # Это список игр для отправки админу
    # players_list = []  # Это список игр для отправки админу
    for game in game_arr:
        games_list.append(game[0])
        # for us_name in game[5]:
        #     one_user = dbase.get_user(us_name)
        #     players_list.append(one_user[3])
        #     players_list.append(one_user[3])
    # for game in game_arr:
    #     one_user = dbase.get_user(game[5][0])
    # print(f"players_list {players_list}")
    return jsonify(games_list)


@app.route("/load_all_new_games")  # Посмотреть список все игр к которым можно присоединиться
@login_required
def load_all_new_games():  # Делаю подпись html, чтоб разделить названия функций с просто запросом страницы
    global game_arr
    # Прочитаем файл со списком игр
    game_arr = dbase.get_all_not_full_games()
    # Выше мы получили кортеж с данными страны, под 5 индексом список ИД игроков
    # Нужно перебрать список ИД игроков и вынести имена игроков
    print(f"game_arr для списка новых игр: {game_arr}")
    games_list = []  # Это список игр для отправки админу game_arr,
    # players_list = []  # Это список игр для отправки админу
    for game in game_arr:
        pls_in_game = []
        for pl in game[5]:
            pls_in_game.append(dbase.get_user(pl)[3])
        game_and_players = [game, pls_in_game]
        games_list.append(game_and_players)
    return jsonify(games_list)


@app.route("/add_player_to_game")  # Посмотреть список все игр к которым можно присоединиться
@login_required
def add_player_to_game():
    game_id = int(request.args.get('id'))
    player_id = int(current_user.get_id())
    player_info = dbase.get_user(player_id)
    print(f"player_info: {player_info}")
    dbase.add_player(game_id, player_id)
    add_dynasty(game_id, player_info)
    return "ok"


@app.route("/delete_game")  # Удалить игру (сделать неактивной)
@login_required
def delete_game():
    user_admin = current_user.get_admin()
    game_id = int(request.args.get('id'))
    if user_admin == 1:
        # list_games = dbase.get_all_games()  # Запросим список игр для теста
        # print(f"list_games: {list_games}")
        dbase.delete_game(game_id)  # Удалим из БД выбранную игру
        # list_games = dbase.get_all_games()  # Запросим список игр для теста
        # print(f"list_games: {list_games}")
    return ""


@app.route("/load_all_my_game")  # Посмотреть список всех игр для игрока
@login_required
def load_all_my_game():  # Делаю подпись html, чтоб разделить названия функций с просто запросом страницы
    global game_arr
    # Прочитаем список игр из БД
    game_arr = dbase.get_all_games()
    player = int(current_user.get_id())
    games_list = []  # Это список игр для отправки игроку для выбора
    print(f"game_arr1: {game_arr}")
    for my_g in game_arr:
        if player in my_g[5]:
            pl_in_game = []
            for pl in my_g[5]:
                pl_in_game.append(dbase.get_user(pl)[3])
            # print(f"Игрок есть в игре номер: {my_g[0]}")
            # Аналог двух append
            one_game = [my_g[0], pl_in_game]
            # games_list.append(f"{my_g[0]} Игроки: {pl_in_game}")
            games_list.append(one_game)
    return jsonify(games_list)


@app.route("/set_active_game")  # Выбор "активной" игры для пользователя, параметры которой будут загружаться
@login_required
def set_active_games():
    game_id = request.args.get('id')
    active_game = int(game_id)
    player = int(current_user.get_id())
    user_name = current_user.get_name()
    # Теперь сохраняем в редиску, можно так и оставить, если будет норм работать
    rediska.set(f"playerID_{player}_active_gameID", active_game)
    print(f"Игрок {user_name} сделал активной игру номер: {active_game}")
    return ""


@app.route("/players")  # Отображение странички со всеми зарегистрированными игроками
@login_required
def players_html():  # Делаю подпись html, чтоб разделить названия функций с просто запросом страницы
    user_admin = current_user.get_admin()
    user_name = current_user.get_name()
    if user_admin == 1:
        return render_template("players.html", title=user_name, menu=menu_admin)
    else:
        return render_template("players.html", title=user_name, menu=menu_auth)


@app.route("/req_list_players")  # Отображение всех зарегистрированных игроков
@login_required
def req_list_players():
    # Поиск игрока по участию в игре. В БД у пользователей планируется запись со списком игр с участием этого игрока
    # Проверка или в тексте запроса к БД. Тут нужен доп аргумент в виде ИД игры
    # Или проверка тут, через цикл по списку каждого пользователя.
    # Подходящие уже тогда добавляются на отправки на фронт
    # who = request.args.get('who')
    list_users_to_front = []
    users = dbase.get_all_user()
    # print(f"users: {users}")
    games = dbase.get_all_games()
    # print(f"games: {games}")
    for user in users:
        # Возвращаем имя пользователя(не логин) и ИД пользователя(для админа)
        # Так же добавим количество побед [5], Имя династии под игрока [6]
        list_users_to_front.append([user[0], user[3], user[5], user[6]])
    return jsonify(list_users_to_front)


@app.route("/req_cities_for_trade")  # Запрос списка городов для торговли
@login_required
def req_cities_for_trade():
    pass


# @app.route("/create_test_new_game")  # Создать "быструю" новую игру по прописаным в коде стартовым параметрам
# @login_required
# def create_test_new_game():
#     user_admin = current_user.get_admin()
#     if user_admin == 1:
#         print("this is admin3")
#         players_dynasty = [[2, "Barkid", "Баркиды"], [3, "Magonid", "Магониды"]]
#         # Передаем дату, чтоб она не обновлялась при "восстановлении" класса игры
#         create_game(players_dynasty)
#         return jsonify("Ответ от Python: Игра создалась")
#     else:
#         return ""


# Создать каждому по одиночной игре
@app.route("/create_new_single_game")
@login_required
def create_new_single_game():
    user_admin = current_user.get_admin()
    if user_admin == 1:
        print("this is admin4")
        users = dbase.get_all_user()
        # print(f"users: {users}")
        for user in users:
            # print(f"user {user[0]}")
            player = int(user[0])
            # [{'playerId': 3, 'nameEng': 'Magonid', 'nameRus': 'Магониды'}]
            players_dynasty = [{'playerId': player, 'nameEng': 'Magonid', 'nameRus': 'Магониды'}]
            # print(players_dynasty)
            create_game(players_dynasty)
        return jsonify("Ответ от Python: Игра создалась")
    else:
        return ""


# Админская версия создания партии
@app.route("/create_new_game_admin", methods=["POST"])  # Создать настроенную игру получив параметры с фронта
@login_required
def create_new_game_admin():
    # Создать вариант, где пользователь не админ, что перекидывало куда-нибудь в другое место
    if request.method == "POST":
        # global game_arr  # Зачем?
        user_admin = current_user.get_admin()
        if user_admin == 1:
            print("this is admin")
            post = request.get_json()
            print(f"post: {post}")
            info_to_front = create_game(post)
            print(f"Ответ от Python: Игра создалась")
            # return jsonify("Ответ от Python: Игра создалась")
            return jsonify(info_to_front)
    else:
        return ""


@app.route("/create_new_game", methods=["POST"])  # Создать настроенную игру получив параметры с фронта
@login_required
def create_new_game():
    if request.method == "POST":
        # Соберем инфу о пользоветеле создавшем игру, его данные будут записаны под первой страной
        player_id = int(current_user.get_id())
        player_info = dbase.get_user(player_id)
        post = request.get_json()
        print(f"post: {post}")
        print(f"player_info: {player_info}")
        setting_for_create_game = [
            {"maxPlayers": post["maxPlayers"]},    # post[0]
            [{"playerId": player_info[0], "nameEng": player_info[6], "nameRus": player_info[6]}]
        ]
        print(f"setting_for_create_game {setting_for_create_game}")
        info_to_front = create_game(setting_for_create_game)
        print(f"Ответ от Python: Игра создалась")
        return jsonify(info_to_front)
    else:
        return ""


def create_game(setting):  # Получаем только список игроков
    # TODO Нужно с фронта получать два аргумента, а не только список
    # all_games = dbase.get_all_games()
    # print(f"all_games: {all_games}")
    global game_arr  # Зачем?
    # Прочитаем файл со списком игр
    game_arr = dbase.get_all_games()
    if len(game_arr) == 0:
        game_arr.append(1)
    else:
        game_arr.append(game_arr[-1][0]+1)  # +1 тут по умолчанию, 0 индекс уже есть, длинна массива 1
    date_now = datetime.strftime(datetime.now(), "%d.%m.%Y %H:%M:%S")  # Дата: день, часы, минуты

    # Создадим мир
    max_pl = setting[0]["maxPlayers"]
    print(f"max_pl: {max_pl}")
    this_game = FirstWorld(game_arr[-1], date_now, max_pl)

    # Создадим папку игры и папку ходов если их не существует
    # Может делать проверку при создании игры, и удалять/создавать заново если она есть
    if not os.path.exists(f"games"):
        os.makedirs(f"games")
    if not os.path.exists(f"games/{game_arr[-1]}"):
        os.makedirs(f"games/{game_arr[-1]}")
    if not os.path.exists(f"games/{game_arr[-1]}/acts"):
        os.makedirs(f"games/{game_arr[-1]}/acts")

    # Создадим династии
    id_players_for_add_db = []  # Массив и ИД игроков, передается в БД, для записи партии
    # print(f"players_dynasty {players_dynasty}")
    num_id = 1
    for player in setting[1]:
        print(f"setting[1]: {setting[1]}")
        print(f"player: {player}")
        # this_game.create_dynasty(1, player[0], player[1], player[2], 10000)  # Золото пока не передается
        # TODO почему первый аргумент всегда 1, надо может делать +1 === num_id Добавить это?
        print(f"Проверка на добавление династии при создании игры")
        this_game.create_dynasty(1, player["playerId"], player["nameEng"], player["nameRus"], 10000)  # Золото пока не передается
        id_players_for_add_db.append(player["playerId"])
        num_id += 1
    # Создадим города
    this_game.create_settlement("Карфаген", "Карфаген")
    this_game.settlements["Карфаген"].goods_in_city.resources_mod_price["Оливки"] = 1
    this_game.settlements["Карфаген"].goods_in_city.resources_mod_price["Медь"] = 2
    this_game.settlements["Карфаген"].goods_in_city.resources_mod_price["Рабы"] = 2
    this_game.settlements["Карфаген"].goods_in_city.resources_mod_price["Шкуры"] = 3
    this_game.settlements["Карфаген"].goods_in_city.resources_mod_price["Зерно"] = 3

    this_game.create_settlement("Сиракузы", "Сиракузы")
    this_game.settlements["Сиракузы"].goods_in_city.resources_mod_price["Оливки"] = 2
    this_game.settlements["Сиракузы"].goods_in_city.resources_mod_price["Медь"] = 3
    this_game.settlements["Сиракузы"].goods_in_city.resources_mod_price["Рабы"] = 1
    this_game.settlements["Сиракузы"].goods_in_city.resources_mod_price["Шкуры"] = 3
    this_game.settlements["Сиракузы"].goods_in_city.resources_mod_price["Зерно"] = 2

    this_game.create_settlement("Афины", "Афины")
    this_game.settlements["Афины"].goods_in_city.resources_mod_price["Оливки"] = 2
    this_game.settlements["Афины"].goods_in_city.resources_mod_price["Медь"] = 3
    this_game.settlements["Афины"].goods_in_city.resources_mod_price["Рабы"] = 2
    this_game.settlements["Афины"].goods_in_city.resources_mod_price["Шкуры"] = 1
    this_game.settlements["Афины"].goods_in_city.resources_mod_price["Зерно"] = 3

    this_game.create_settlement("Родос", "Родос")
    this_game.settlements["Родос"].goods_in_city.resources_mod_price["Оливки"] = 3
    this_game.settlements["Родос"].goods_in_city.resources_mod_price["Медь"] = 1
    this_game.settlements["Родос"].goods_in_city.resources_mod_price["Рабы"] = 3
    this_game.settlements["Родос"].goods_in_city.resources_mod_price["Шкуры"] = 2
    this_game.settlements["Родос"].goods_in_city.resources_mod_price["Зерно"] = 2

    this_game.create_settlement("Александрия", "Александрия")
    this_game.settlements["Александрия"].goods_in_city.resources_mod_price["Оливки"] = 3
    this_game.settlements["Александрия"].goods_in_city.resources_mod_price["Медь"] = 2
    this_game.settlements["Александрия"].goods_in_city.resources_mod_price["Рабы"] = 3
    this_game.settlements["Александрия"].goods_in_city.resources_mod_price["Шкуры"] = 2
    this_game.settlements["Александрия"].goods_in_city.resources_mod_price["Зерно"] = 1

    this_game.create_settlement("Тир", "Тир")
    this_game.settlements["Тир"].goods_in_city.resources_mod_price["Оливки"] = 2
    this_game.settlements["Тир"].goods_in_city.resources_mod_price["Медь"] = 2
    this_game.settlements["Тир"].goods_in_city.resources_mod_price["Рабы"] = 2
    this_game.settlements["Тир"].goods_in_city.resources_mod_price["Шкуры"] = 2
    this_game.settlements["Тир"].goods_in_city.resources_mod_price["Зерно"] = 2
    # print(this_game.settlements["Карфаген"].goods_in_city)
    # print(this_game.settlements["Сиракузы"].goods_in_city)
    # print(this_game.settlements["Афины"].goods_in_city)
    # print(this_game.settlements["Родос"].goods_in_city)
    # this_game.create_settlement("Athens", "Афины")
    # this_game.create_settlement("Alexandria", "Александрия")
    # this_game.create_settlement("Tyr", "Тир")
    # this_game.create_settlement("Syracuse", "Сиракузы")

    this_game.save_to_file()
    # setting[1] это список династий, агрументом отдаем его длину как текущее количество игроков
    print("Добавляем игру в БД")
    dbase.add_game(1, -300, id_players_for_add_db, len(setting[1]), max_pl)

    print("Игра создана")
    print(this_game.dynasty_list)
    return f"Game create {setting[1]}"


def add_dynasty(game_id, player):
    game = FirstWorld(game_id)  # Восстановим саму игру.
    game.load_from_file(game_id)  # Запустим метод считающий данные из файла.
    # TODO исправить первый аргумент???
    # TODO так же исправить количество золота
    game.create_dynasty(1, player[0], player[6], player[6], 10000)
    game.save_to_file()


# !!!!!!!!!! Отменять надо у Активной игры. Или нет?
@app.route("/cancel_act")  # Отменить акт(действие). Все или последний. !!! Доработать возможность выбора любого
def cancel_act():
    what = request.args.get('what')
    # response = dbase.read_router_comment(id_router)
    player = int(current_user.get_id())
    # Получим ИД партии !!!!!!!!!!!! Обязательно проверку
    game_id = request.args.get('gameId')
    try:  # Блок на случай отсутствия файла
        with open(f"games/{game_id}/gameID_{game_id}_playerID_{player}.trader", 'rb') as f:
            data = pickle.load(f)
            if what == "all":
                data["acts"] = []
            elif what == "last":
                data["acts"].pop(-1)
            with open(f"games/{game_id}/gameID_{game_id}_playerID_{player}.trader", 'wb') as new_f:
                pickle.dump(data, new_f, pickle.HIGHEST_PROTOCOL)
        return "ok"
    except FileNotFoundError:
        print(f"Файл 'games/{game_id}/gameID_{game_id}_playerID_{player}.trader' не найден")
        return ""


# Отображение в меню дипломатии всех игроков с основными параметрами(золото, имя, готовность хода)
@app.route("/req_status_all_player", methods=["GET"])
@login_required
def req_status_all_player():
    game_id = request.args.get('gameId')
    return_data = []
    try:
        with open(f"games/{game_id}/gameID_{game_id}.trader", 'rb') as f:
            data_players = pickle.load(f)
    except FileNotFoundError:
        print(f"Файл 'games/{game_id}/gameID_{game_id}.trader' не найден")
        return ""
    for player_id in data_players["player_list"]:
        try:
            with open(f"games/{game_id}/gameID_{game_id}_playerID_{player_id}.trader", 'rb') as f:
                data_one_player = pickle.load(f)
                one_player = {
                    "name_rus": data_one_player["name_rus"],
                    "gold": data_one_player["gold"],
                    # "donate_sum": data_one_player["donate_sum"],
                    # "title": data_one_player["title"],
                    "end_turn": data_one_player["end_turn"],
                    "win_points": data_one_player["win_points"],
                    # "body_points": data_one_player["body_points"],
                }
                return_data.append(one_player)
        except FileNotFoundError:
            print(f"Файл 'games/{game_id}/gameID_{game_id}_playerID_{player_id}.trader' не найден")
            return ""
    return jsonify(return_data)


@app.route("/req_status_game_player", methods=["GET"])  # Запрос параметров страны игрока
@login_required
def req_status_game_player():
    player = int(current_user.get_id())
    game_id = rediska.get(f'playerID_{player}_active_gameID')
    # Выходит что нам не нужно обращаться к классу Династии запуская ее метод
    try:
        with open(f"games/{game_id}/gameID_{game_id}_playerID_{player}.trader", 'rb') as f:
            data = pickle.load(f)
            print(data)
    except FileNotFoundError:
        print(f"Файл 'games/{game_id}/gameID_{game_id}_playerID_{player}.trader' не найден")
        return ""
    return jsonify(data)


@app.route("/req_status_game", methods=["GET"])  # Запрос общих параметров партии
@login_required
def req_status_game():
    player = int(current_user.get_id())
    user_name = current_user.get_name()
    game_id = rediska.get(f'playerID_{player}_active_gameID')
    # print(f"ИД игры при запросе статуса династии: {game_id}")
    # !!!!!!!!! Тут еще нужна проверка на существование самой партии
    try:
        with open(f"games/{game_id}/gameID_{game_id}.trader", 'rb') as f:
            my_world = pickle.load(f)
    except FileNotFoundError:
        print(f"Файл 'games/{game_id}/gameID_{game_id}.trader' не найден")
        return ""
    print(f"my_world: {my_world}")
    # Так же загрузим список городов для торговли
    cities = Cities()
    list_cities = cities.cities_available()
    goods = Goods()
    buildings = ColonyBuildings()
    goods_name_list = goods.resources_available()
    buildings_name_list = buildings.buildings_name_list
    # print(f"goods_name: {goods_name}")
    data = {
            # Об игроках
            "max_players": my_world["max_players"],
            "dynasty_list": my_world["dynasty_list"],
            "winners": my_world["winners"],  # need_win_points_for_win
            "need_win_points_for_win": my_world["need_win_points_for_win"],
            "year": my_world["year"],
            "turn": my_world["turn"],
            "all_logs": my_world["all_logs"],
            "all_logs_party": my_world["all_logs_party"],
            "game_id": my_world["row_id"],
            "date_create": my_world["date_create"],
            "buildings_price": my_world["buildings_price"],
            "all_goods_prices": my_world["all_goods_prices"],
            "user_name": user_name,
            "cities": list_cities,
            "goods_name_list": goods_name_list,
            "buildings_name_list": buildings_name_list,
            "donate_leader": my_world["donate_leader"],
        }
    print(f"data {data}")
    return jsonify(data)


# !!!!!!!!!!!!! Запустить функцию подсчета хода
@app.route("/post_turn", methods=["POST"])  # Подтверждение готовности хода
@login_required
def post_turn():
    if request.method == "POST":
        # print('Запрос с js')
        # Определим игрока, чтоб понять от кого получен ход и куда его записать
        player = int(current_user.get_id())
        # Получим ИД партии, ей будем присваивать ход !!!!!!!!!!!! после проверки
        # !!!!!!!!! Нужна проверка участвует ли игрок в этой игре!!!!!!!!!!!!!!!!!!!!!!!!!!
        game_id = request.args.get('gameID')
        # print(f"ИД партии которой передается ход: {game_id}")
        # Получаем список с действиями игрока
        try:
            with open(f"games/{game_id}/gameID_{game_id}_playerID_{player}.trader", 'rb') as f:
                data = pickle.load(f)
        except FileNotFoundError:
            print(f"Файл 'games/{game_id}/gameID_{game_id}_playerID_{player}.trader' не найден")
            return ""
        # Присвоим ход игроку
        data["end_turn"] = True
        # Снова запишем ход
        with open(f"games/{game_id}/gameID_{game_id}_playerID_{player}.trader", 'wb') as f:
            pickle.dump(data, f, pickle.HIGHEST_PROTOCOL)
        world.check_readiness(game_id)
    # Временно возвращаем пустую строку
    return ""


@app.route("/post_act", methods=["POST"])  # Отправка одного акта(действия) игрока
@login_required
def post_act():
    """
        Отдельная функция получения одного действия.
        Необходима для отображения актуального списка действий,
        который не будет пропадать и сбиваться при обновлении странички.
        Ход при этом не считается отправленным.
    """
    if request.method == "POST":
        # print('Запрос с js')
        # Определим игрока, чтоб понять от кого получен ход и куда его записать
        player = int(current_user.get_id())
        # Получим ИД партии, ей будем присваивать акт !!!!!!!!!!!! после проверки
        game_id = request.args.get('gameID')
        # !!!!!!!!! Нужна проверка участвует ли игрок в этой игре!!!!!!!!!!!!!!!!!!!!!!!!!!
        # Получаем список с действиями игрока
        post = request.get_json()
        # Прочитаем файл игрока
        try:
            with open(f"games/{game_id}/gameID_{game_id}_playerID_{player}.trader", 'rb') as f:
                data = pickle.load(f)
        except FileNotFoundError:
            print(f"Файл 'games/{game_id}/gameID_{game_id}_playerID_{player}.trader' не найден")
            return ""
        # Присвоим ход игроку
        data["acts"] = post
        # Снова запишем ход
        with open(f"games/{game_id}/gameID_{game_id}_playerID_{player}.trader", 'wb') as f:
            pickle.dump(data, f, pickle.HIGHEST_PROTOCOL)
    # Временно возвращаем пустую строку
    return ""


@app.route("/confirm_rec_turn", methods=["GET"])  # Подтверждение готовности хода
@login_required
def confirm_rec_turn():
    # print('Запрос с js')
    # Определим игрока, чтоб понять от кого получен запрос и куда его записать
    player = int(current_user.get_id())
    # Получим ИД партии, ей будем присваивать запрос !!!!!!!!!!!! после проверки
    # !!!!!!!!! Нужна проверка участвует ли игрок в этой игре!!!!!!!!!!!!!!!!!!!!!!!!!!
    game_id = request.args.get('gameID')
    # print(f"ИД партии которой передается ход: {game_id}")
    # Получаем список с действиями игрока
    try:
        with open(f"games/{game_id}/gameID_{game_id}_playerID_{player}.trader", 'rb') as f:
            data = pickle.load(f)
    except FileNotFoundError:
        print(f"Файл 'games/{game_id}/gameID_{game_id}_playerID_{player}.trader' не найден")
        return ""
    # Присвоим изменения игроку
    data["end_turn_know"] = True
    # Снова запишем в файл
    with open(f"games/{game_id}/gameID_{game_id}_playerID_{player}.trader", 'wb') as f:
        pickle.dump(data, f, pickle.HIGHEST_PROTOCOL)
    world.check_readiness(game_id)


@app.route("/contact", methods=["POST", "GET"])  # Обратная связь
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


@app.route("/login", methods=["POST", "GET"])  # Авторизация
def login():
    if current_user.is_authenticated:
        return redirect(url_for('profile'))
    if request.method == "POST":
        user = dbase.get_user_by_login(request.form['login'].lower())
        # user = user
        if user and check_password_hash(user[2], request.form['psw']):
            user_login = UserLogin().create(user)
            login_user(user_login)
            print(f"Текущий пользователь:", current_user.get_id())
            return redirect(request.args.get("next") or url_for("profile"))
        flash("Wrong login/password", category="error")
        print("Ошибка авторизации")

    return render_template('login.html',  title="Авторизация", menu=menu)


@app.route('/logout')  # Выход из профиля
@login_required
def logout():
    logout_user()
    flash("Вы вышли из аккаунта", "success")
    return redirect(url_for('login'))


@app.route('/profile')  # Отображение странички профиля
@login_required
def profile():
    user_admin = current_user.get_admin()
    if user_admin == 1:
        print("this is admin")
        return render_template("profile.html", title="Профиль", menu=menu_admin)
    return render_template("profile.html", title="Профиль", menu=menu_auth)


if __name__ == '__main__':
    app.run(debug=True)
