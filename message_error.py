from enum import Enum


class DETAILERROR(str, Enum):
    NOT_FOUND = 'not found'
    CANNOT_UPDATE = 'You cannot update this'
    CANNOT_DELETE = 'You cannot delete this'

    INCORRECT_EMAIL_OR_PASSWORD = 'Incorrect email or password'
    USER_WITH_THIS_EMAIL_EXISTS = 'User with this email exists'
    NOT_VALIDATE_CREDENTIALS = 'Could not validate credentials'

    def obj(self, txt):
        return f'{txt} {self.value}'

    @property
    def article(self):
        return f'{self.value} article'

    @property
    def comment(self):
        return f'{self.value} comment'

    @property
    def user(self):
        return f'{self.value} user'
