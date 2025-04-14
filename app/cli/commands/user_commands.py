from ..command import Command
from dao import UserDAO
from models import User

class CreateUserCommand(Command):
    def __init__(self, session, user_data: dict):
        self.session = session
        self.user_dao = UserDAO(session)
        self.user_data = user_data
        self.created_user = None

    def execute(self):
        user = User(**self.user_data)
        self.created_user = self.user_dao.create(instance=user)
        return self.created_user

    def undo(self):
        if self.created_user:
            self.user_dao.delete(self.created_user.user_id)
    
    def description(self):
        return f"Created user {self.user_data['email']}"
    
class LoginCommand(Command):
    def __init__(self, session, email, password):
        self.session = session
        self.email = email
        self.password = password
        self.user = None

    def execute(self):
        user_dao = UserDAO(self.session)
        self.user = user_dao.authenticate(self.email, self.password)
        return self.user

    def undo(self):
        pass

    def description(self):
        return f"User login: {self.email}"