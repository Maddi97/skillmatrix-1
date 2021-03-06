"""Contains the Milestone API"""
import json
import traceback
from flask import Response
from flask_restful import Resource, reqparse
from controller.controller import controller


class Milestone(Resource):
    """The Milestone-API takes the given milestone and user, hands them to the backend controller"""

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("comment", type=str)
        parser.add_argument("date", type=str)
        parser.add_argument("level", type=int)
        parser.add_argument("skillpath", type=str)
        parser.add_argument("username", type=str)
        args = parser.parse_args()
        message = json.dumps(controller.add_milestone(args["username"],
                                                      args["skillpath"],
                                                      args["date"],
                                                      args["comment"],
                                                      args["level"]))
        try:
            return Response(message, status=200, mimetype="application/json")
        except TimeoutError:
            return Response(status=504)
        except PermissionError:
            return Response(status=401)
        except Exception:
            traceback.print_exc()
            return Response(status=520)

    def options(self):
        pass
