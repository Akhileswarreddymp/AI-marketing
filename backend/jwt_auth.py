import jwt
from fastapi import APIRouter,Request, HTTPException
import time
from decouple import config
from fastapi.security import HTTPBearer,HTTPAuthorizationCredentials

router = APIRouter()

JWT_SECRET = config("secret")
JWT_ALGORITHM = config("algorithm")

def token_resp(token: str):
    return {
        "access_token": token
    }


def signJWT(userId: str):
    expiration_time = time.time() + 600
    print("userId",userId)
    try:
        user_id = userId.decode()
    except Exception as e:
        user_id = userId
    payload = {
        "userId": user_id,
        "exp": expiration_time
    }

    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    print(token_resp(token))
    return token_resp(token)

def decodeJWT(token: str):
    try:
        decoded_token = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        print("decoded_token",decoded_token)
        exp_claim = decoded_token.get('exp')
        
        if exp_claim is None:
            return {"error": "'exp' claim is missing in the token"}
        
        return decoded_token if exp_claim >= time.time() else None
    except:
        return {"error": "Token has expired"}
    

class jwtBearer(HTTPBearer):
    def __init__(self, auto_Error :bool = True):
        super(jwtBearer,self).__init__(auto_error=auto_Error)


    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super().__call__(request)
        if not credentials.scheme == "Bearer":
            print("credentials.scheme", credentials.scheme)
            raise HTTPException(status_code=403, detail="Invalid or Expired Token!!")
        print("credentials.credentials",credentials.credentials)
        if not self.verify_jwt(credentials.credentials):
            raise HTTPException(status_code=403, detail="Invalid Token")

        return credentials.credentials
        
    def verify_jwt(self, jwtoken: str) -> bool:
        try:
            payload = decodeJWT(jwtoken)
            return True
        except HTTPException:
            return False 

