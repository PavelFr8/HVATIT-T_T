from data import db_session
from data.users import User
from flask_restful import abort, Resource
from flask import jsonify
from .reqparse2 import parser


def abort_if_user_not_found(user_id):
    sess = db_session.create_session()
    users = sess.query(User).get(user_id)
    if not users:
        abort(404, message=f"User {user_id} not found")


class UsersResource(Resource):
    def get(self, user_id):
        abort_if_user_not_found(user_id)
        sess = db_session.create_session()
        users = sess.query(User).get(user_id)
        return jsonify(
            {
                'user': users.to_dict(only=(
                    'surname', 'name', 'age'))
            }
        )

    def delete(self, user_id):
        abort_if_user_not_found(user_id)
        sess = db_session.create_session()
        users = sess.query(User).get(user_id)
        sess.delete(users)
        sess.commit()
        return jsonify({'success': 'OK'})


class NewsListResource(Resource):
    def get(self):
        sess = db_session.create_session()
        users = sess.query(User).all()
        return jsonify(
            {
                'user': [item.to_dict(only=(
                    'surname', 'name', 'age')) for item in users]
            }
        )

    def post(self):
        args = parser.parse_args()
        sess = db_session.create_session()
        users = User(
            surname=args['surname'],
            name=args['name'],
            age=args['age'],
            position=args['position'],
            speciality=args['speciality'],
            address=args['address'],
            hashed_password=args['hashed_password'],
            email=args['email'],
        )
        sess.add(users)
        sess.commit()
        return jsonify({'success': 'OK'})

