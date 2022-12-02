class UserLogin:
    def fromDB(self, user_id, db):
        self.__user = db.get_user(user_id)
        return self

    def create(self, user):
        self.__user = user
        return self

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        # return str(self.__user['id'])
        # Возвращаю строку. Это нормально?
        # Можно преобразовывать в инт при запросе
        return str(self.__user[0])

    def get_admin(self):
        print("Проверка на админку UserLogin.py set_admin")
        return int(self.__user[4])

    def get_name(self):
        # return str(self.__user['name'])
        return str(self.__user[3])
