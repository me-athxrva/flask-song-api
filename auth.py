from flask import request
from flask_restful import Resource
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from db import db, User

# User Registration Resource
class UserRegistration(Resource):
    def post(self):
        data = request.get_json()
        username = data['username']
        password = data['password']

        if not username or not password:
            return {'error':'Missing username or password'}, 400
        elif User.query.filter_by(username=username).first():
            return {'message':f'This username already exists'}, 400
        else:
            new_user = User(username=username, password=password)
            db.session.add(new_user)
            db.session.commit()

            user = User.query.filter_by(username=username).first()
            if user:
                access_token = create_access_token(identity=str(user.username))
                return {'access_token': access_token}, 200

# User Login Resource
class UserLogin(Resource):
    def post(self):
        data = request.get_json()
        username = data['username']
        password = data['password']

        user = User.query.filter_by(username=username).first()

        if not username or not password:
            return {'error': 'missing credentials'}, 400
        elif user and user.password==password:
            access_token = create_access_token(identity=str(user.username))
            return {'status': 'logged in','access_token':access_token}, 200
        else:
            return {'message':'invalid credentials'}, 400

# Check user authentication
@jwt_required()
def is_authenticated():
    current_user = get_jwt_identity()
    user = User.query.filter_by(username=current_user).first()
    if user.username:
        return True 
    else:
        return False