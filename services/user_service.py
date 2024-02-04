from repositories.user_repository import user_repository

class UserService:
    def __init__(self, user_repository):
        self.user_repository = user_repository

    def register_user(self, name, password, role):
        return self.user_repository.register(name, password, role)

    def login_user(self, name, password):
        self.user_repository.login(name, password)

    def return_user(self):
        self.user_repository.get_user()

    def logout_user(self):
        self.user_repository.logout_user()

    def check_role(self, role):
        self.user_repository.require_role(role)

    def get_user_id(self):
        self.user_repository.get_user()

    def check_csrf(self):
        self.user_repository.check_csrf()

user_service = UserService(user_repository)