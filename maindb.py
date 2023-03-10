
from flask import Flask, render_template, request, flash, g, redirect, url_for, jsonify
import psycopg2
from flask_login import login_required, current_user, login_user, LoginManager, logout_user

import config
from FDataBase import FDataBase
from UserLogin import UserLogin

#
# Debug = True
# SECRET_KEY = config.SECRET_KEY
#
# app = Flask(__name__)
# app.config.from_object(__name__)

# login_manager = LoginManager(app)
# login_manager.login_view = "login"
# login_manager.login_message = "Необходимо авторизоваться"
# login_manager.login_message_category = 'error'


def get_db():
    if not hasattr(g, 'link_db'):
        g.link_db = connect_db()
        # print("Соединение не было создано")
    # print("Соединение не было создано и мы его создали")
    return g.link_db


# @app.teardown_appcontext
# def close_db(error):
#     # Закрываем соединение с БД, если оно было установлено
#     if hasattr(g, 'link_db'):
#         g.link_db.close()


dbase = None


# @app.before_request
def before_request():
    # Database connection, before query
    global dbase
    db = get_db()
    dbase = FDataBase(db)


def connect_db():
    connect = psycopg2.connect(
        host=config.host,
        user=config.user,
        password=config.password,
        database=config.db_name
    )
    return connect
