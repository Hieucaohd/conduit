# from flask import Blueprint
# from src.api.urls import Endpoint
# from src.api import HttpMethod
# from src.common.utils.alchemy import execute_sql
# user = Blueprint("user",__name__)
# @user.route(Endpoint.USER1, methods=[HttpMethod.POST])
# def authenticate_user() : 
#     pass 

# @user.route(Endpoint.USER, method=[HttpMethod.POST])
# def create_user():
#     user1 = {
#     "user":{
#     "email": "jake@jake.jake",
#     "password": "jakejake"
#     }
#     }
#     state=f"""INSERT INTO conduit.author(username,password)
#     VALUES ('{user['user']['email']}','{user['user']['password']})"""
#     execute_sql(state) 
#     return "created user successfully"

# @user.route(Endpoint.USER, method=[HttpMethod.GET])
# def get_current_user():
#     pass

# @user.route(Endpoint.USER, methods=[HttpMethod.PUT])
# def update_user():
#     pass

# @user.route(Endpoint.USER2, methods=[HttpMethod.GET])
# def get_profile(slug):
#     pass 

# @user.route(Endpoint.USER3, methods=[HttpMethod.POST])
# def follow_user(slug):
#     pass 

# @user.route(Endpoint.USER3, methods=[HttpMethod.DELETE])
# def unfollow_user(slug):
#     pass 
