from app.auth.exceptions import EmailAlreadyExists, InvalidCredentials, UsernameAlreadyExists, InactiveUser
from app.auth.models import User
from app.extensions import db

class AuthService:
    
    def create_user(self, username: str, email: str, password: str) -> User:
        if User.query.filter_by(email=email).first():
            raise EmailAlreadyExists()
        
        if User.query.filter_by(username=username).first():
            raise UsernameAlreadyExists()
        
        user = User(username=username, email=email)
        user.set_password(password)
        
        db.session.add(user)
        db.session.commit()

        return user

    def authenticate(self, email: str, password: str) -> User:
        user = User.query.filter_by(email=email).first()

        if not user:
            raise InvalidCredentials()
        
        if not user.active:
            raise InactiveUser()
        
        if not user.check_password(password):
            raise InvalidCredentials()
        
        return user
    
auth_service = AuthService()
