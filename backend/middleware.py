import fastapi
import glob
import json
import os
import importlib
from fastapi.middleware.cors import CORSMiddleware
from typing import Union

app = fastapi.FastAPI()

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
    payload_data = request.json()
    print("payload_data====>",payload_data)
    print(request.method)
    response = fastapi.Response(None, status_code=403)
    allowed_paths = [
        '/api/users/verify_otp',
        '/api/users/register',
        '/api/users/send_otp',
        "/docs",
        "/openapi.json",
        
    ]
    if request.method == "OPTIONS":
        return await call_next(request)
    if request.url.path in allowed_paths:
        return await call_next(request)
    
    cookie_value = request.cookies.get(cookie_name)
    print("request_headers=",request.headers)
    print(f"Cookie Name: {cookie_name}")
    print(f"Cookie Value: {cookie_value}")

    # if not cookie_value:
    #     redirect_url = f"https://{request.base_url.hostname}/login"
    #     print("redirect_url",redirect_url)
    #     # response: fastapi.responses.Response = await call_next(request)
    #     response = fastapi.responses.JSONResponse({'url': redirect_url}, status_code=401)

    return response

