from typing import List

from flask_jwt_extended import jwt_required
from flask_restplus import Resource, Namespace, fields, reqparse
from flask_sqlalchemy_session import current_session
from sqlalchemy.orm import joinedload

from app.models import Town, District

api = Namespace('towns', decorators=[jwt_required])


town_model = api.model('Town', {
    'town_id': fields.Integer(),
    'name': fields.String(),
    'district_id': fields.Integer(),
})

town_payload_model = api.model('Town Payload', {
    'name': fields.String(),
    'district_id': fields.Integer(),
})


@api.route('/<int:town_id>')
@api.response(404, description='Town not found')
@api.doc(security='JWT Access')
@api.response(401, 'Missing Authorization Header')
class TownItem(Resource):

    @api.marshal_with(town_model)
    def get(self, town_id) -> Town:
        return current_session.query(Town).get(town_id)

    @api.expect(town_payload_model)
    @api.marshal_with(town_model)
    def patch(self, town_id) -> Town:
        current_session.query(Town).filter_by(town_id=town_id).update(api.payload)
        current_session.commit()
        town = current_session.query(Town).get(town_id)
        return town

    @api.response(204, 'Town deleted.')
    def delete(self, town_id):
        current_session.query(Town).filter_by(town_id=town_id).delete()


@api.route('/')
@api.doc(security='JWT Access')
@api.response(401, 'Missing Authorization Header')
class TownCollection(Resource):

    query_parser = reqparse.RequestParser()
    query_parser.add_argument('district_id', type=int)

    @api.expect(query_parser)
    @api.marshal_with(town_model, as_list=True, envelope='towns')
    def get(self) -> List[Town]:
        district_id = self.query_parser.parse_args().get('district_id')
        if district_id is None:
            return current_session.query(Town).all()

        return current_session.query(Town).filter(Town.district_id.in_(get_subdistricts(district_id))).all()

    @api.expect(town_payload_model)
    @api.marshal_with(town_model)
    def post(self) -> Town:
        town = Town(**api.payload)
        current_session.add(town)
        current_session.commit()
        return town


def get_subdistricts(*district_ids):
    if not len(district_ids):
        return []
    district_ids = list(district_ids)
    sub_districts = current_session.query(District).filter(District.parent_district_id.in_(district_ids)).all()
    sub_district_ids = [district.district_id for district in sub_districts]
    return district_ids + get_subdistricts(*sub_district_ids)
