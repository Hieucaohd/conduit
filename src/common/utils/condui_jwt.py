import jwt  
from flask import request 
def encode(user_credentials ) :
    encode_jwt = jwt.encode(user_credentials,"secret",algorithm="HS256")
    return encode_jwt

def decode(encode) : 
    decode_jwt = jwt.decode(encode,"secret",algorithms=['HS256'])
    return decode_jwt


# jwt.decode(encode_jwt,"secret",algorithms=['HS256'])
# jwt.encode(payload, key, algorithm="HS256", headers=None, json_encoder=None)
# jwt.decode(jwt, key="", algorithms=None, options=None, audience=None, issuer=None, leeway=0)


# def get_header() : 
#     authorization = request.headers.get('Authorization')
#     return authorization 




