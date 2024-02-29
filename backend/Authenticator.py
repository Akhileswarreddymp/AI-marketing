from fastapi import APIRouter,HTTPException,responses
from models import *
from mongo import *
import hashlib
import random
import smtplib
from email.message import EmailMessage
import uuid
from jwt_auth import *

router = APIRouter(prefix='/users')


@router.post("/register",tags=['user'])
async def user_register(data :register_params ):
    redis_client = await redisConnection()
    temp_mail = redis_client.setex(f"{data.email}_email", 3000, data.email)
    temp_username = redis_client.setex(f"{data.email}_username", 3000, data.username)
    hash_temp_password = hashlib.md5(data.password.encode('utf-8')).hexdigest()
    temp_password = redis_client.setex(f"{data.email}_password", 3000,hash_temp_password)
    collection = await dbconnect('user_auth','users')
    res = collection.find_one({"email": data.email})
    if res:
        return {
            "msg":"user already exist"
        }
    await send_otp(redis_client.get(f"{data.email}_email").decode())
    redis_client.close()
    return {
            "msg":"Details stored in redis"
        }



@router.post("/send_otp", tags=["OTP"])
async def send_otp(request: otp_email):
    if not isinstance(request,str):
        d = dict(request)
        request = d.get("email")
    print("send_mail_data",request)
    otp_generated = random.randint(10000,99999)
    s = smtplib.SMTP('smtp.gmail.com', 587)
    # start TLS for security
    s.starttls()
    s.login("akhileswarreddymp@gmail.com", "xodgydwslhywjare")

    message = EmailMessage()
    message["Subject"] = "Verificaion code to change password"
    message = f"Your verification cod is {otp_generated}"
    s.subject = "Verification code"

    s.sendmail("akhileswarreddymp@gmail.com",request, message)
    print("akhileswarreddymp@gmail.com", request, message)
    print("Mail sent sucessfully")
    s.quit()
    await redis_store(otp_generated,request)
    return {"msg" : "mail Sent Successfully"}


async def redis_store(otp,email):
    redis_client = await redisConnection()
    key = f"{email}_otp"
    value = otp
    ttl = 3000
    redis_client.setex(key, ttl, value)
    print("opt saved==>",redis_client.get(key))
    redis_client.close()



@router.post('/verify_otp',tags=['OTP'])
async def verifyOtp(request : only_otp):
    data = request
    print("otpdata===>",data.otp)
    redis_client = await redisConnection()
    stored_otp = redis_client.get(f"{data.email}_otp").decode()
    print("stored_otp=====>",stored_otp)
    email_id = redis_client.get(f"{data.email}_email").decode()
    user_name = redis_client.get(f"{data.email}_username").decode()
    user_password = redis_client.get(f"{data.email}_password").decode()

    if data.otp == stored_otp:
        collection = await dbconnect('user_auth','users')
        user_data = {
            "email" :email_id ,
            "name" : user_name,
            "password" : user_password
        }
        add_user = collection.insert_one(user_data)
        print("add_user===>",add_user)
        print("user created successfully")
        redis_client.close()
        return {"msg" : "user created successfully"}

async def check_user(data):
    password = hashlib.md5(data.password.encode('utf-8')).hexdigest()
    collection = await dbconnect('user_auth','users')
    result = collection.find_one({"email": data.email})
    if result and result.get("email") == data.email and result.get("password") == password:
        return True
    else:
        return False




@router.post('/login',tags=['Authentication'])
async def Userlogin(data : login_params):
    cookie_name = "access_token"
    if await check_user(data):
        cookie_id = str(uuid.uuid4())
        access_token =  signJWT(data.email)
        redis_client = await redisConnection()
        store_cookie_id = redis_client.hset("CookieStore", cookie_id, "useraccesstoken." + access_token["access_token"])
        response = responses.JSONResponse({"status": "Logged in Successfully","access_token" : access_token}, status_code=200)
        response.set_cookie(cookie_name,cookie_id, path="/", expires=3600, samesite="Lax", secure=True)
        redis_client.close()
        return response
    else:
        raise HTTPException(status_code=401, detail="Wrong Credentials received")



@router.post('/forgot-password',tags=['Authentication'])
async def forgotPassword(data : forgotPassword_params):
    redis_client = await redisConnection()
    print(redis_client.get(f"{data.email}_otp"),data.otp)
    if redis_client.get(f"{data.email}_otp").decode() == data.otp:
        if data.newpassword == data.confirm_Password:
            collection = await dbconnect('user_auth','users')
            result = collection.find_one({"email": data.email})
            filter = {"_id":result.get("_id")}
            new_password = hashlib.md5(data.newpassword.encode('utf-8')).hexdigest()
            update_field = collection.update_one(filter,{'$set': {"password":new_password}})
            redis_client.close()
            return {"msg": "Password Updated Successfully"}
        else:
            redis_client.close()
            raise HTTPException(status_code=401, detail="New Password and re entred password are not matched")
        redis_client.close()
    else:
        redis_client.close()
        raise HTTPException(status_code=401, detail="Incorrect OTP")
    


@router.post('/reset-password',tags=['Authentication'])
async def resetPassword(data : resetPassword_params):
    collection = await dbconnect('user_auth','users')
    result = collection.find_one({"email": data.email})
    oldPassword = result.get("password")
    print("filter====>",oldPassword)
    user_entred_password = hashlib.md5(data.old_password.encode('utf-8')).hexdigest()
    if oldPassword == user_entred_password:
        filter = {"_id":result.get("_id")}
        if data.new_password == data.confirm_password:
            new_pass = hashlib.md5(data.new_password.encode('utf-8')).hexdigest()
            update_field = collection.update_one(filter,{'$set': {"password":new_pass}})
            return {"msg": "Password Updated Successfully"}
        else:
            raise HTTPException(status_code=401, detail="New Password and re entred password are not matched")
    else:
        raise HTTPException(status_code=401, detail="Received incorrect password")
    
    
