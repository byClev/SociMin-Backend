class AuthError(Exception):
    """Base de todos os erros de auth"""

class EmailAlreadyExists(AuthError):
    pass

class UsernameAlreadyExists(AuthError):
    pass

class InvalidCredentials(AuthError):
    pass

class InactiveUser(AuthError):
    pass