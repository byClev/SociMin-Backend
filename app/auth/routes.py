from app.auth import bp

@bp.route('/login', methods=['POST'])
def login():
    return {'message': 'Login endpoint'}, 200

@bp.route('/register', methods=['POST'])
def register():
    return {'message': 'Register endpoint'}, 200

@bp.route('/logout', methods=['POST'])
def logout():
    return {'message': 'Logout endpoint'}, 200