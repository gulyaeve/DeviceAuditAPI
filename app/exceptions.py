from fastapi import HTTPException, status


class BaseAPIException(HTTPException):
    status_code = 500
    detail = ""

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class UserAlreadyExistsException(BaseAPIException):
    status_code = status.HTTP_409_CONFLICT
    detail = "User exists"


class IncorrectEmailOrPasswordException(BaseAPIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Wrong email or password"


class TokenAbsentException(BaseAPIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "No token"


class TokenExpiredException(BaseAPIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Expired token"


class IncorrectTokenFormatException(BaseAPIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Wrong token format"


class UserIsNotPresentException(BaseAPIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Пользователь не найден"


class WrongTokenException(BaseAPIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Bearer token missing or unknown"


class DatabaseIntegrityError(BaseAPIException):
    status_code = status.HTTP_409_CONFLICT
    detail = "Integration error / model conflict"


class EntityNotExistsException(BaseAPIException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Entity does not exists"
