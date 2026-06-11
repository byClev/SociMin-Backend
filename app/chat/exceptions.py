class ChatException(Exception):
    pass

class ChatNotFound(ChatException):
    pass    

class UnauthorizedAccess(ChatException):
    pass

class ChatAlreadyExists(ChatException):
    pass