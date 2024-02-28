import jwt
import time
from decouple import config

JWT_SECRET = config("JWT_SECRET")
JWT_ALGORITHM = config("JWT_ALGORITHM")

def token_resp(token: str):
    return {
        "access_token": token
    }

def signJWT(userId: str):
    # expiration_time = time.time() + 600
    try:
        user_id = userId.decode()
    except AttributeError:
        user_id = userId
    payload = {
        "userId": user_id
    }

    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return "Bearer " + token_resp(token)["access_token"]

def decodeJWT(token: str):
    try:
        decoded_token = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        # exp_claim = decoded_token.get('exp')
        
        # if exp_claim is None:
        #     return {"error": "'exp' claim is missing in the token"}
        
        return decoded_token 
    except jwt.ExpiredSignatureError:
        return {"error": "Token has expired"}
    except jwt.InvalidTokenError:
        return {"error": "Invalid token"}
    




