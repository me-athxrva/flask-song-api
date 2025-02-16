from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from datetime import timedelta
from auth import UserLogin, UserRegistration
from resourcefetch import GetSongsList, GetSong, StreamSong
from db import db

# Flask app initialization
app = Flask(__name__)

# App Configurations
app.config['SECRET_KEY'] = 'n1k2n4jn53kjnjkn12njk2JKN@N#!NKN$k1jn4j2nk2nj4njk13'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['JWT_SECRET_KEY'] = 'ajvjksdbvjkabj24j53b4jk3bjjk263bk35j2b6k235bk6'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(minutes=60)

# app declarations
db.init_app(app)
api = Api(app)
CORS(app)
jwt = JWTManager(app)

# creating database
with app.app_context():
    db.create_all()

# adding api resources
api.add_resource(UserRegistration,'/api/register')
api.add_resource(UserLogin,'/api/login')
api.add_resource(GetSongsList,'/api/getsongslist')
api.add_resource(GetSong,'/api/getsong')
api.add_resource(StreamSong,'/api/stream/<string:song_name>')

# runs app
if __name__ == '__main__':
    app.run()