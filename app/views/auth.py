from flask_jwt_extended import create_access_token, create_refresh_token, jwt_refresh_token_required, get_jwt_identity
from flask_restplus import Namespace, fields, Resource
from flask_sqlalchemy_session import current_session
from sqlalchemy.orm.exc import NoResultFound

from app.models import User

api = Namespace('auth')

auth_model = api.model('Auth Payload', {
    'name': fields.String(max_length=32, required=True),
    'password': fields.String(max_length=32, required=True),
})

token_pair = api.model('JWT Token Pair', {
    'access': fields.String(),
    'refresh': fields.String(),
})


def pwd_hash(password):
    # TODO: Add password hashing
    return password


def invalidate_previous_tokens(user_id):
    # TODO: Add invalidation of previous tokens
    pass


@api.route('/sign-up')
class SignUpController(Resource):

    @api.expect(auth_model)
    def post(self):
        # TODO: Add email or phone verification
        print(api.payload)
        new_user = User(name=api.payload['name'], password_hash=pwd_hash(api.payload['password']))
        current_session.add(new_user)
        current_session.commit()


@api.route('/sign-in')
@api.response(401, 'Invalid Credentials')
class SignInController(Resource):

    @api.expect(auth_model)
    @api.marshal_with(token_pair)
    def post(self):
        try:
            user = current_session.query(User).filter_by(name=api.payload['name']).one()
        except NoResultFound:
            api.abort(404, f'User with name {api.payload["name"]} not found.')
        if user.password_hash == pwd_hash(api.payload['password']):
            invalidate_previous_tokens(user.user_id)
            access_token = create_access_token(identity=user.user_id, fresh=True)
            refresh_token = create_refresh_token(identity=user.user_id)
            return {
                'access': access_token,
                'refresh': refresh_token,
            }

        return {'message': 'Invalid Credentials!'}, 401


@api.route('/refresh')
@api.doc(security='JWT Refresh')
@api.response(401, 'Missing Authorization Header')
class RefreshController(Resource):

    @jwt_refresh_token_required
    @api.marshal_with(token_pair)
    def post(self):
        user_id = get_jwt_identity()
        invalidate_previous_tokens(user_id)
        return {
            'access': create_access_token(identity=user_id, fresh=True),
            'refresh': create_refresh_token(identity=user_id),
        }
