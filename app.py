from flask import Flask, request
from flask_restful import Resource, Api
from flask_jwt_extended import JWTManager, create_access_token, get_jwt_claims, jwt_required
import user_service
from sqlite3 import IntegrityError

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'my-ultra-secret-key-that-would-be-hidden-in-production'
api = Api(app)
users = {}
jwt = JWTManager(app)
db = None


@app.before_first_request
def init_db():
    user_service.init_db()


@jwt.user_claims_loader
def add_claims_to_access_token(identity):
    return {
        'username': identity['username'],
        'user_type': identity['user_type'],
        'department': identity['department']
    }


class Login(Resource):
    def get(self):
        username = request.headers['username']
        password = request.headers['password']
        if username and password:
            logged_in = user_service.get_user_info(username, password)
            if logged_in:
                identity = {'username': logged_in['username'],
                            'user_type': logged_in['user_type'],
                            'department': logged_in['department']}
                access_token = {'access_token': create_access_token(identity)}
                return access_token
            else:
                return 'That username/password combination is not in our system', 401


class UserList(Resource):
    @jwt_required
    def get(self):
        claims = get_jwt_claims()
        username = claims['username']
        user_type = claims['user_type']
        department = claims['department']
        if user_type == 'MANAGER':
            return user_service.get_managed_users(username)
        elif department == 'HR':
            return user_service.get_non_hr_users()
        elif user_type == 'ADMIN':
            return user_service.get_all_users()
        else:
            return user_service.get_user(username)

    @jwt_required
    def post(self):
        claims = get_jwt_claims()
        user_type = claims['user_type']
        department = claims['department']
        if user_type == 'ADMIN' or department == 'HR':
            try:
                user = {
                    'username': request.json['username'],
                    'password': request.json['password'],
                    'department': request.json['department'],
                    'user_type': request.json['user_type'],
                    'manager_username': request.json['manager_username'],
                    'salary': request.json['salary'],
                    'annual_bonus': request.json['annual_bonus'],
                    'vacation_history': request.json['vacation_history']
                }
                user_service.insert_user(user)
                return user
            except KeyError:
                return 'You haven\'t provided all necessary information', 400
            except IntegrityError:
                return 'This user already exists in the system. Maybe try updating them?', 400
        else:
            return 'Not allowed to create user', 401


class User(Resource):
    @jwt_required
    def put(self, user):
        claims = get_jwt_claims()
        username = claims['username']
        user_type = claims['user_type']
        department = claims['department']
        if user_type == 'ADMIN' or user_type == 'MANAGER' or department == 'HR':
            try:
                user_editing = user_service.get_user_if_can_edit(user_type, department, username, user)
                user_editing = user_editing[0]
                for key, value in request.json.items():
                    if key == 'salary':
                        user_editing[key] = value
                        user_service.update_user_salary(user, value)
                    elif key in user_editing:
                        user_editing[key] = value
                    else:
                        print(key)
                        return 'badly formatted json', 400
                user_service.replace_user(user_editing)
                return user_editing
            except TypeError:
                return 'this user does not exist or you do not have permission to edit them', 401
        else:
            return 'you are not authorized to edit users', 401


class SalaryHist(Resource):
    @jwt_required
    def get(self, user):
        claims = get_jwt_claims()
        username = claims['username']
        user_type = claims['user_type']
        department = claims['department']
        if user_type == 'ADMIN' or user_type == 'MANAGER' or department == 'HR':
            try:
                user_salary = user_service.get_salary_if_can_view(user_type, department, username, user)
                return user_salary
            except TypeError:
                return 'you are not authorized to view this user\'s salary or this user doesn\'t have any salary history', 401

        else:
            return 'you are not authorized to view user salaries', 401


api.add_resource(UserList, '/users')
api.add_resource(Login, '/login')
api.add_resource(SalaryHist, '/salaries/<string:user>')
api.add_resource(User, '/user/<string:user>')


if __name__ == '__main__':
    app.run()
