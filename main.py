from flask import Flask, render_template, request, flash, g, redirect, url_for, jsonify
import psycopg2
import postgreTables
from datetime import datetime
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import login_required, current_user, login_user, LoginManager, logout_user

import config
from FDataBase import FDataBase
from world import FirstWorld
from UserLogin import UserLogin


Debug = True
SECRET_KEY = config.SECRET_KEY

app = Flask(__name__)
app.config.from_object(__name__)

login_manager = LoginManager(app)
login_manager.login_view = "login"
login_manager.login_message = "Необходимо авторизоваться"
login_manager.login_message_category = 'error'

menu = [{"name": "Авторизация", "url": "login"},
        # {"name": "Игра", "url": "game"},
        {"name": "Feedback", "url": "contact"}]

menu_auth = [{"name": "Профиль", "url": "profile"},
             {"name": "Игра", "url": "game"},
             {"name": "Feedback", "url": "contact"}]

menu_admin = [{"name": "Профиль", "url": "profile"},
              {"name": "Игра", "url": "game"},
              {"name": "Создать игру", "url": "create-game"},
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
game = None


@app.before_request
def before_request():
    # Database connection, before query
    global dbase
    db = get_db()
    dbase = FDataBase(db)


@login_manager.user_loader
def load_user(user_id):
    print("Load user")
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
    # Проверим на админку и проверим на наличие созданной игры
    if user_admin == 1:
        print("this is admin2")
        if game is not None:
            # Если игра создана, отобразим базовый интерфейс, с бека понятно никакие параметры не загрузятся
            return render_template("game.html", title=user_name, menu=menu_admin)
        else:  # Если игра не создана перекинуть на окошко создания новой игры
            return render_template("create-game.html", title=user_name, menu=menu_admin)
    else:
        if game is not None:  # Если игра создана откроем страничку игры, после произойдет запрос с фронта параметров
            return render_template('game.html',  title=user_name, menu=menu_auth)
        else:  # Если игра не создана, перекинем на страничку присоединения к новой игре
            return render_template('new-game.html', title=user_name, menu=menu_auth)


@app.route("/create_new_game")
@login_required
def create_new_game():
    user_admin = current_user.get_admin()
    if user_admin == 1:
        print("this is admin3")
        # Создадим игру, пока она одна, позже проработать возможность создания нескольких
        global game
        game = FirstWorld(1)
        game.create_dynasty(1, 2, "Barkid", "Баркиды", 10000)
        game.create_dynasty(2, 3, "Magonid", "Магониды", 12000)
        # Так же присвоим одноименным переменным созданные династии
        print("Игра на двоих создана")
        Barkid = game.dynasty['Barkid']
        print(game.dynasty['Barkid'])
        print(Barkid.name_rus)
        Magonid = game.dynasty['Magonid']
        print(Magonid)
        print(game.dynasty['Magonid'])
        print(game.dynasty_list)
        print(game.dynasty["Barkid"].player_id)
        print(game.dynasty["Magonid"].player_id)
        # print(game1["Barkid"])
        # print(game1.Barkid)
        # return game
    return render_template("create-game.html", title="Main", menu=menu_admin)


# def create_game():
#     pass


@app.route("/req_status_game_player", methods=["GET"])
@login_required
def req_status_game_player():
    global game
    if game is not None:
        player = int(current_user.get_id())
        # Определим принадлежность игры к игроку через цикл, пройдясь по параметру player_id
        # Сравним с ид игрока, если совпадает запрашиваем и отправляет параметры
        for i in game.dynasty_list:
            if player == game.dynasty[i].player_id:
                print(f"Наша страна: {game.dynasty[i].name_rus}")
                var_to_front = game.dynasty[i].return_var()
                print(game.dynasty[i].return_var())
                return jsonify(var_to_front)
    #     return jsonify(game.var_for_front(cur_game))
    return ""


@app.route("/req_status_game", methods=["GET"])
@login_required
def req_status_game():
    global game
    if game is not None:
        data = {
            "year": game.year,
            "turn": game.turn,
        }
        return jsonify(data)
    else:
        return ""


@app.route("/post_turn", methods=["POST"])
@login_required
def post_turn():
    global game
    if request.method == "POST":
        print('Запрос с js')
        # Тут нужно получить переменные с фронта
        # Определим игрока, чтоб понять от кого получен ход и куда его записать
        player = int(current_user.get_id())
        # Определим принадлежность игры к игроку через цикл, пройдясь по параметру player_id
        # Сравним с ид игрока, если совпадает запрашиваем и отправляет параметры
        # !!! А чего, напрямую нельзя присвоить??? Используя dynasty[player]
        # Можно =) НЕТТТ
        # game.dynasty[player].end_turn = True
        for i in game.dynasty_list:
            if player == game.dynasty[i].player_id:
                # Получаем список с действиями игрока
                post = request.get_json()
                print(post)
                # Присваиваем список действий игрока конкретному игроку
                game.dynasty[i].acts = post
                # Меняем переменную отвечающую за готовность хода
                game.dynasty[i].end_turn = True
        # Запускаем саму обработку хода, там будет доп проверка все ли игроки прислали ход
        game.calculate_turn()
    # Временно возвращаем пустую строку
    return ""


@app.route("/post_act", methods=["POST"])
@login_required
def post_act():
    """
        Отдельная функция получения одного действия.
        Необходима для отображения актуального списка действий,
        который не будет пропадать и сбиваться при обновлении странички.
        Ход при этом не считается отправленным.
    """
    global game
    if request.method == "POST":
        print('Запрос с js')
        # Тут нужно получить переменные с фронта
        # Определим игрока, чтоб понять от кого получен ход и куда его записать
        player = int(current_user.get_id())
        # Определим принадлежность игры к игроку через цикл, пройдясь по параметру player_id
        # Сравним с ид игрока, если совпадает запрашиваем и отправляет параметры
        for i in game.dynasty_list:
            if player == game.dynasty[i].player_id:
                # Получаем список с действиями игрока
                post = request.get_json()
                print(post)
                # Присваиваем список действий игрока конкретному игроку
                game.dynasty[i].acts = post
                # Меняем переменную отвечающую за готовность хода
    # Временно возвращаем пустую строку
    return ""


@app.route("/contact", methods=["POST", "GET"])
@login_required
def contact():
    if request.method == "POST":
        # Feedback is available only to authorized users
        if len(request.form['message']) > 3:
            flash('Message sent', category="success")
            # Неправильна форма глагола send, sent прошедшее время в утвердительной форме
            dbase.add_feedback(request.form['message'], 1)  # 1 это фейковый ид юзера
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
        # print(user[2])
        # print(request.form['psw'])
        if user and check_password_hash(user[2], request.form['psw']):
            user_login = UserLogin().create(user)
            login_user(user_login)
            print(f"Текущий пользователь:", current_user.get_id())

            # return redirect(url_for('index'))
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


# postgreTables.create_tables()

if __name__ == '__main__':
    app.run(debug=True)
