from fastapi import FastAPI,APIRouter,HTTPException
from models import *
from mongo import *
import hashlib
import random
import smtplib
from email.message import EmailMessage

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
    await send_otp(redis_client.get(f"{data.email}_mail").decode())
    redis_client.close()
    return {
            "msg":"Details stored in redis"
        }



@router.post("/send_otp", tags=["Authentication"])
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
    #sending otp text in this format
    message = f"Your verification cod is {otp_generated}"
    s.subject = "Verification code"
    # send mail
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


\

@router.post('/verify_otp',tags=['Authentication'])
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
        print("user_data=====>",user_data)
        print("user created successfully")
        return {"msg" : "user created successfully"}




