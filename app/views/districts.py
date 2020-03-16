from collections import defaultdict
from typing import List

from flask import current_app
from flask_jwt_extended import jwt_required
from flask_restplus import Namespace, fields, Resource
from flask_sqlalchemy_session import current_session

from app.models import District

api = Namespace('districts', description='(Проверку на цикличность дистриктов не делал)', decorators=[jwt_required])


district_model = api.model('District', {
    'district_id': fields.Integer(),
    'name': fields.String(),
    'parent_district_id': fields.Integer(),
})

district_payload_model = api.model('District Payload', {
    'name': fields.String(),
    'parent_district_id': fields.Integer(),
})

district_tree_model = api.model('District Tree', {
    'districts_tree': fields.List(fields.Nested(api.model('District Node', {
        'district_id': fields.Integer(),
        'name': fields.String(),
        'sub_districts': fields.List(fields.Raw(title='District Node')),
    }))),
})


@api.route('/<int:district_id>')
@api.response(404, description='District not found')
@api.doc(security='JWT Access')
@api.response(401, 'Missing Authorization Header')
class DistrictItem(Resource):

    @api.marshal_with(district_model)
    def get(self, district_id) -> District:
        return current_session.query(District).get(district_id)

    @api.expect(district_payload_model)
    @api.marshal_with(district_model)
    def patch(self, district_id) -> District:
        current_session.query(District).filter_by(district_id=district_id).update(api.payload)
        current_session.commit()
        district = current_session.query(District).get(district_id)
        return district

    @api.response(204, 'District deleted.')
    def delete(self, district_id):
        current_session.query(District).filter_by(district_id=district_id).delete()


@api.route('/')
@api.doc(security='JWT Access')
@api.response(401, 'Missing Authorization Header')
class DistrictCollection(Resource):

    @api.marshal_with(district_model, as_list=True, envelope='districts')
    def get(self) -> List[District]:
        return current_session.query(District).all()

    @api.expect(district_payload_model)
    @api.marshal_with(district_model)
    def post(self) -> District:
        district = District(**api.payload)
        current_session.add(district)
        current_session.commit()
        return district


@api.route('/tree')
@api.doc(security='JWT Access')
@api.response(401, 'Missing Authorization Header')
class DistrictTree(Resource):

    @api.response(200, 'Success', district_tree_model)
    def get(self) -> List[District]:

        def district_recursive_model(max_deep=None):
            if max_deep is None:
                max_deep = current_app.config['DISTRICTS_TREE_MAX_DEEP']
            tree_fields = {
                'district_id': fields.Integer(),
                'name': fields.String(),
            }
            if max_deep:
                tree_fields['sub_districts'] = fields.List(fields.Nested(district_recursive_model(max_deep - 1)))
            return api.model(f'Districts Tree {max_deep}', tree_fields)

        def prepare_tree(root_district):
            return {
                'district_id': root_district.district_id,
                'name': root_district.name,
                'sub_districts': [
                    prepare_tree(sub_district) for sub_district in sub_districts_map[root_district.district_id]
                ],
            }

        districts = current_session.query(District).all()
        sub_districts_map = defaultdict(list)
        roots = []
        for district in districts:
            if district.parent_district_id is None:
                roots.append(district)
            else:
                sub_districts_map[district.parent_district_id].append(district)

        return api.marshal(
            [prepare_tree(district) for district in roots],
            district_recursive_model(),
            envelope='districts_tree',
        )
