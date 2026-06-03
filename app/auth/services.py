from app.auth.models import User
from app.extensions import db

class AuthService:
    @staticmethod
    def create_user(username, email, password):
        # Aqui você adicionaria a lógica de hash de senha (ex: bcrypt)
        user = User(username=username, email=email)
        # user.set_password(password)
        db.session.add(user)
        db.session.commit()
        return user
