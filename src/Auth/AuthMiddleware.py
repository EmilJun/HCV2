from functools import wraps
from flask import g, request
import jwt
from src.Auth.AuthRepository import AuthRepository
from src.Auth.IAuthModel import IAuthModel
from src.User.UserRepository import UserRepository
from src.User.IUserRepo import IUserRepo
from src.__Parents.Service import Service
from src import app


class AuthMiddleware(Service):
    __auth_repository: IAuthModel = AuthRepository()
    __user_repository: IUserRepo = UserRepository()

    @staticmethod
    def check_authorize(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            try:
                decode = jwt.decode(request.headers['Authorization'].split(' ')[1],
                                    app.config['JWT_SECRET_KEY'],
                                    algorithms=[app.config['JWT_ALGORITHM']])
            except:
                return AuthMiddleware.response_invalid_login()

            if decode and AuthMiddleware.__auth_repository.get_by_user_id(decode['user_id']):
                user = AuthMiddleware.__user_repository.get_by_id(user_id=decode['user_id'], client_id=None)
                g.user = user
                g.user_id = user.id
                g.client_id = user.client_id

                return f(*args, **kwargs)
            return AuthMiddleware.response_invalid_login()

        return decorated_function

    # @staticmethod
    # def check_authorize(f):
    #     @wraps(f)
    #     @jwt_required()
    #     def decorated_function(*args, **kwargs):
    #
    #         auth = AuthMiddleware.__auth_repository.get_by_user_id(user_id=get_jwt_identity())
    #         if auth['access_token'] == request.headers['authorization'].split(' ')[1]:
    #
    #             if AuthMiddleware.__user_repository.get_by_id(auth['user_id']):
    #                 g.user_id = get_jwt_identity()
    #                 return f(*args, **kwargs)
    #
    #         return Service.response_invalid_login()
    #     return decorated_function
mjbm
