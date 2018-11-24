'''The rest_api module provides REST-APIs for communication to the SkillMatrix frontend.'''
import parentdir
from flask import Flask, Response
import json
from flask_restful import Resource, Api, reqparse
from src.authentication import Authentication
import database_manager

app = Flask(__name__)
api = Api(app)
parser = reqparse.RequestParser()

class Login(Resource):
    '''Login-API deserializes JSON and hands it to the Authentication class of authentication module'''
    def post(self):
        parser.add_argument("username", type=str)
        parser.add_argument("password", type=str)   
        args = parser.parse_args()
        try:
            return Authentication.login(self,args["username"], args["password"])
        except AttributeError:
            return Response(status=400)
        except TimeoutError:
            return Response(status=504)
        except Exception:
            return Response(status=520)

class Logout(Resource):
    '''Login-API deserializes JSON and hands it to the Authentication class of authentication module'''
    def post(self):
        parser.add_argument("username", type=str)
        args = parser.parse_args()
        try:
            Authentication.logout(self,args["username"])
            return Response(status=200)
        except Exception:
            return Response(status=520)
            
class Search(Resource):
    '''Search-API deserializes the query. 
    Takes id of the searching user and an array of skills (currently only one term)'''
    def post(self):
        parser.add_argument("query", type=str)
        args = parser.parse_args()
        try:
            return database_manager.handle_query(self,args["query"])
        except ValueError:
            return json.dumps(list())

api.add_resource(Login, "/login")
api.add_resource(Logout, "/logout")

if __name__ == "__main__":
    app.run(debug=True)