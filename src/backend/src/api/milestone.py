"""Contains the Milestone API"""
import set_root_backend
from src.controller.controller import controller
from flask import Response
from flask_restful import Resource, reqparse


class Milestone(Resource):
    """The Milestone-API takes the given milestone and user, hands them to the backend controller"""

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("username", type=str)
        parser.add_argument("skill", type=str)
        parser.add_argument("level", type=int)
        parser.add_argument("date", type=str)
        parser.add_argument("comment", type=str)
        args = parser.parse_args()
        message = controller.add_milestone(self,
                                           args["username"],
                                           args["skill"],
                                           args["date"],
                                           args["comment"],
                                           args["level"]).replace("\\", "")
        try:
            return Response(message, status=200, mimetype="application/json")
        except TimeoutError:
            return Response(status=504)

    def options(self):
        pass
