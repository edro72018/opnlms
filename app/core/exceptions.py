class LMSException(Exception):
    def __init__(self, message: str, status_code: int = 400):
        self.message = message
        self.status_code = status_code


class NotFoundError(LMSException):
    def __init__(self, resource: str = "Recurso"):
        super().__init__(f"{resource} no encontrado", 404)


class ForbiddenError(LMSException):
    def __init__(self):
        super().__init__("No tienes permiso para esta acción", 403)


class AuthError(LMSException):
    def __init__(self, msg: str = "Credenciales inválidas"):
        super().__init__(msg, 401)
