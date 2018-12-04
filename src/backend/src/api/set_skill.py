"""Contains the SetSkill API"""
import set_root_backend
from src.controller.controller import controller
from flask import Response
from flask_restful import Resource, reqparse


class SetSkill(Resource):
    """The SetSkill-API takes the query arguments and hands them over to the backend controller"""

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("username", type=str)
        parser.add_argument("skills", type=dict)
        args = parser.parse_args()
        try:
            message = controller.set_skills(self, args["username"], args["skills"])
            return Response(message, status=200, mimetype="application/json")
        except TimeoutError:
            return Response(status=504)

    def options(self):
        pass