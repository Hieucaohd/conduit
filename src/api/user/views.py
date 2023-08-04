from flask import Blueprint, request, jsonify
from src.api.urls import Endpoint
from src.api import HttpMethod
from src.common.utils.alchemy import execute_sql,execute_sql2
from src.common.utils.condui_jwt import encode, decode

blueprint = Blueprint("user", __name__)


@blueprint.route(Endpoint.USER, methods=[HttpMethod.POST])
def create_user():
    data = request.get_json()
    email = data.get('user', {}).get('email')
    password = data.get('user', {}).get('password')
    # Check if the user already exists in the database
    existing_user = check_user_exists(email)
    if existing_user:
        return jsonify({"message": "User already exists."})
    else:
        insert_user(email, password)
        user_credentials = {'username': email}
        encode_token = encode(user_credentials)
        return {
                "user": {
                    "email": f"{email}",
                    "token": f"{encode_token}",
                    "username": "jake",
                    "bio": "I work at statefarm",
                    "image": None
                        }
                }

def check_user_exists(email):
    result = execute_sql(
        f"""SELECT username from conduit.author WHERE username = '{email}'""")
    if result:
        return True
    else:
        return False

def insert_user(email, password):
    execute_sql2(
        f""" INSERT INTO conduit.author(username,password) VALUES ('{email}','{password}')""")
 
@blueprint.route(Endpoint.USER1, methods=[HttpMethod.POST])
def login_user():
    data = request.get_json()
    email = data.get('user', {}).get('email')
    password = data.get('user', {}).get('password')
    user_credentials = {'username': email}
    result1 = check_username(email)
    if result1:
        if check_password(email, password):
            encode_token = encode(user_credentials) 
            return {
                    "user": {
                        "email": f"{email}",
                        "token": f"{encode_token}",
                        "username": "jake",
                        "bio": "I work at statefarm",
                        "image": None
                            }
                    }
        else:
            return jsonify({'message': 'check your password again'})
    else:
        return jsonify({'message': 'username does not existed'})

def check_username(email):
    state = f"""SELECT username,password from conduit.author WHERE username = '{email}' """
    result = execute_sql(state)
    if result:
        return True
    else:
        return False

def check_password(email, password):
    state = f"""SELECT password FROM conduit.author WHERE username = '{email}' """
    result = execute_sql(state)
    if password == result[0]["password"]:
        return True
    else:
        return False


@blueprint.route(Endpoint.USER4, methods=[HttpMethod.GET])
def get_current_user():
    to = request.headers.get('Authorization')
    token = to[6:]
    if not token:
        return jsonify({"message":"your token is not commited or incorrect"})
    jwt_token = decode(token) 
    username = jwt_token['username']
    if not username :
        return jsonify({"message":"invalid token"})
    state = f"""SELECT username,bio,image FROM conduit.author WHERE username='{username}'"""
    result =  execute_sql(state) 
    result_main = result[0] 
    result_main['token'] = token 
    result_main['email'] = username 
    return {"user":result_main 
    }

@blueprint.route(Endpoint.USER4, methods=[HttpMethod.PUT])
def update_user():
    to = request.headers.get('Authorization')
    token = to[6:] 
    if not token :
        return jsonify({"message":"your token is not commited or not correct"})
    jwt_token = decode(token)
    username = jwt_token['username']
    if not username : 
        return jsonify({"message":"invalid token"})
    data = request.get_json()
    bio = data.get('user', {}).get('bio')
    image = data.get('user', {}).get('image')
    email = data.get('user', {}).get('email')
    username_get = data.get('user', {}).get('username')

    state = f"UPDATE conduit.author SET bio='{bio}' , image='{image}',email='{email}',username='{username_get}' WHERE username ='{username}'"
    execute_sql2(state) 
    return {
            "user": 
            {
                "email": f"{email}",
                "token": f"{to}",
                "username": f"{username}",
                "bio": f"{bio}",
                "image": f"{image}"
            }
            }


@blueprint.route(Endpoint.USER2, methods=[HttpMethod.GET])
def get_profile(username):
    state = f""" SELECT username,bio,image FROM conduit.author WHERE username ='{username}' """
    result = execute_sql(state)
    result_main = result[0]
    result_main['following'] = False
    return {'profile' : result_main
        }  
    

@blueprint.route(Endpoint.USER3, methods=[HttpMethod.POST])
def follow_user(au_username):
    to = request.headers.get("Authorization")
    token = to[6:] 
    if not token :
        return jsonify({"message":"your token is not commited or invalid"})
    jwt_token = decode(token)
    user_username = jwt_token['username']
    if not user_username : 
        return jsonify({'message':'check your token'})
    state = f"""INSERT INTO conduit.followed(author_username,user_username) VALUES ('{au_username}','{user_username}')"""
    execute_sql2(state)
    state1 = f""" SELECT username,bio,image FROM conduit.author WHERE username ='{au_username}' """
    result = execute_sql(state1)
    result_main = result[0]
    result_main['following'] = False
    return {'profile' : result_main
        }   
    
    
@blueprint.route(Endpoint.USER3, methods=[HttpMethod.DELETE])
def unfollow_user(au_username):
    to = request.headers.get("Authorization")
    token = to[6:]
    if not token : 
        return jsonify({"message":"your token is not commited or invalid"})
    jwt_token = decode(token) 
    user_username = jwt_token['username']
    if not user_username : 
        return jsonify({'message':"check your token again"})
    state = f"""DELETE FROM conduit.followed 
WHERE author_username = '{au_username}' AND user_username = '{user_username}'"""
    execute_sql2(state) 
    state1 = f""" SELECT username,bio,image FROM conduit.author WHERE username ='{au_username}' """
    result = execute_sql(state1)
    result_main = result[0]
    result_main['following'] = False
    return {'profile' : result_main
        }   
