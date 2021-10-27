from datetime import datetime, timedelta
from flask import Flask
from flask.helpers import make_response
from flask import request
from flask.json import jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import session
import jwt

app = Flask(__name__)
app.config['SECRET_KEY'] = 'thisismyflasksecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:0000@localhost/Login'
db = SQLAlchemy(app)



class User(db.Model):
    
    __tablename__ = 'Users'



    id = db.Column('id', db.Integer, primary_key=True)



    login = db.Column('login', db.String(50))



    password = db.Column('password', db.String(50))



    token = db.Column('token', db.String(255))



    def __init__(self,id,login, password, token):



        self.id = id

        self.login = login

        self.password = password

        self.token = token  
    
    def verify(loginAttempt, passwordAttempt):
        loginQuery = User.query.filter_by(login=loginAttempt).first()
        if loginQuery != None and loginQuery.password == passwordAttempt:
            return True
        else: False
    
    def verifyToken(Token):
        loginQuery = User.query.filter_by(token=Token).first()
        if loginQuery != None:
            return True
        else: False

    def saveToken(loginAttempt, Token):
        loginQuery = User.query.filter_by(login=loginAttempt).first()
        loginQuery.token = Token
        db.session.commit()

 

# use code bellow to create table and insert data in your database
# db.create_all()


# new_users = [User(0, 'Asset', 'Asset123456', 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyIjoidXNlciIsImV4cCI6MTYzNTM0MzA1MH0.Ij_MQ-4OeFikggAnCVXZ-0ZPbDtg7jGk0sNKLZCoVEs'),
# User(1, 'Baha', 'Asset123456', 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyIjoidXNlciIsImV4cCI6MTYzNTM0MzIwNX0.6M_YCMs2V7vMfgAkm4Aa9u9V_7iv6CqgEP63GyXXSMM'),
# User(2, 'Batyr', 'Asset123456', 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyIjoidXNlciIsImV4cCI6MTYzNTM0MzIzOX0.gx_DzKuKjywFJ2uoXSOmo6ICRJoZKbapyZST_75jy6I')]

# for user in new_users:
#     db.session.add(user)


@app.route('/login')
def login():

    auth = request.authorization
    if auth:
        if User.verify(auth.username, auth.password):
            token = jwt.encode({'user':auth.username, 'exp':datetime.utcnow() + timedelta(minutes=30)}, app.config['SECRET_KEY'])
            User.saveToken(auth.username, token)
            return jsonify({'token': token, 'Login': auth.username})
        else:
            return '<h1> : Could not found a user with login: <login> </h1>'
    return make_response('Could not verify!', 401, {'WWW-Authenticate': 'Basic realm="Login required'})


@app.route('/protected', methods=['GET', 'POST'])
def protected():
    token = request.args.get('token')
    if User.verifyToken(token):
        return '<h1>Hello, token which is provided is correct </h1>'
    else:
        return '<h1>Hello, Could not verify the token </h1>'    



if __name__ == '__main__':
    app.run(debug=True)


    