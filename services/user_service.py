from sqlalchemy.sql import text
from repositories.user_repository import user_repository
from entities.db import db


class UserService:
    """ Responsible for communication between the database and the the session. """

    def __init__(self, user_repository):
        self.user_repository = user_repository
        self.db = db

    def register_user(self, name, password, role):
        return self.user_repository.register(name, password, role)

    def login_user(self, name, password):
        self.user_repository.login(name, password)

    def logout_user(self):
        self.user_repository.logout_user()

    def check_role(self, role):
        self.user_repository.require_role(role)

    def get_user_id(self):
        return self.user_repository.get_user()

    def check_csrf(self):
        self.user_repository.check_csrf()

    def get_username(self, u_id):
        query = "SELECT name FROM users WHERE id=:id"
        return self.db.session.execute(text(query), {"id": u_id}).fetchone()


user_service = UserService(user_repository)
