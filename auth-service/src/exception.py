from fastapi import status


class AppException(Exception):
    status_code: int


class UserNotFound(AppException):
    status_code: int = status.HTTP_404_NOT_FOUND

    def __str__(self):
        return "Пользователь с таким логином не найден"


class UserExists(AppException):
    status_code: int = status.HTTP_409_CONFLICT

    def __str__(self):
        return "Пользователь с таким логином уже существует"


class WrongPassword(AppException):
    status_code: int = status.HTTP_409_CONFLICT

    def __str__(self):
        return "Неправильный пароль"


class TokenException(AppException):
    status_code: int = status.HTTP_401_UNAUTHORIZED

    def __init__(self, msg: str, *args):
        super().__init__(*args)
        self.msg = msg

    def __str__(self):
        return f"Ошибка токена: {self.msg}"


class BrokenToken(AppException):
    status_code: int = status.HTTP_401_UNAUTHORIZED

    def __str__(self):
        return "Некорректный токен"
