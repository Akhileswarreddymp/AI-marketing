import fastapi
import glob
import json
import os
import importlib
from fastapi.middleware.cors import CORSMiddleware
from typing import Union
from fastapi.responses import JSONResponse
import jwt
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
from decouple import config

app = fastapi.FastAPI()


JWT_SECRET = config("JWT_SECRET")
JWT_ALGORITHM = config("JWT_ALGORITHM")

app.on_event("startup")
def onstart():
    for filename in glob.glob("**/*.py", recursive=True):
        if filename.startswith("."):
            continue
        #get all the file in the directory
        modname = os.path.splitext(filename)[0].replace(os.sep, '.')
        #get file path using importlib
        mod = importlib.import_module(modname)
        # to get attr named router 
        symbol = getattr(mod, 'router', None)
        if isinstance(symbol, fastapi.APIRouter):
            app.include_router(symbol, prefix="/api")
        else:
            for attr in dir(mod):
                if not attr.startswith("_"):
                    symbol = getattr(mod, attr)
                    if isinstance(symbol, fastapi.APIRouter):
                        app.include_router(symbol, prefix="/api")

onstart()

origins = [
    "http://localhost",
    "http://localhost:8001",
    "http://127.0.0.1:8001",
    "http://127.0.0.1:5500",
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

cookie_name = "Akhil"

@app.middleware('http')
async def authMiddleware(request: fastapi.Request, call_next):
    response = fastapi.Response(None, status_code=403)
    allowed_paths = [
        '/api/users/verify_otp',
        '/api/users/register',
        '/api/users/send_otp',
        "/docs",
        "/openapi.json",
        "/api/users/login",
    ]

    if request.method == "OPTIONS":
        return await call_next(request)
    requested_path = request.url.path
    if requested_path in allowed_paths:
        return await call_next(request)
    elif any(requested_path.startswith(path.rstrip('/')) for path in allowed_paths):
        return await call_next(request)

    authorization: str = request.headers.get('access_token')
    if not authorization or not authorization.startswith("Bearer "):
        return JSONResponse({"detail": "Not authenticated"}, status_code=401)
    token = authorization.replace("Bearer ", "")
    try:
        decoded_token = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        request.state.user = decoded_token.get("userId")
        return await call_next(request)
    except InvalidTokenError:
        return JSONResponse({"detail": "Invalid token"}, status_code=401)


