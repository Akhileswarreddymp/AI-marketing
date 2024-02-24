from fastapi import APIRouter
import pydantic
from mongo import *
import random
router = APIRouter()

class user(pydantic.BaseModel):
    user : str

@router.post('/userCreate',tags=["practice_user"])
async def userCreate(request : user):
    if not isinstance(request,dict):
        data = dict(request)
    else:
        data = request
    user_id = request.user + str(random.randint(1000,9999))
    print(user_id)
    data["user_id"] = user_id
    collection = await dbconnect('practice_user','practice_user')
    create_user = collection.insert_one(data)
    return {"msg" : "User Created Successfully"}



@router.get("/get_user",tags=["practice_user"])
async def get_user_data():
    collection = await dbconnect("practice_user","practice_user")
    cursor = collection.find()
    user_data = []
    for doc in cursor:
        doc['_id'] = str(doc['_id'])
        user_data.append(doc)
    return user_data

class user_id(pydantic.BaseModel):
    user_id : str

@router.post("/get_user_id", tags=["practice_user"])
async def get_user_by_id(request : user_id):
    if not isinstance(request,dict):
        request = dict(request)
    else: 
        request = request
    query1 = {'user_id': request.get("user_id")}
    collection = await dbconnect("practice_user","practice_user")
    cursor = collection.find(query1)
    user_data = []
    for doc in cursor:
        # Convert ObjectId to string
        doc['_id'] = str(doc['_id'])
        user_data.append(doc)
    return user_data



@router.post("/delete_user",tags=["practice_user"])
async def delete_user(request : user_id):
    if not isinstance(request,dict):
        request = dict(request)
    else: 
        request = request
    query1 = {'user_id': request.get("user_id")}
    collection = await dbconnect("practice_user","practice_user")
    cursor = collection.delete_one(query1)
    print(cursor)
    output = await get_user_data()

    return output

class update_userP(pydantic.BaseModel):
    user_id : str
    user_name : str

@router.post("/update_user",tags=["practice_user"])
async def update_user(request : update_userP):
    # user_data = {}
    filter = {'user_id': request.user_id}
    # data = await get_user_by_id({"user_id" : request.user_id})
    # if data:
    #     user_data["user"] = request.user_name
    #     user_data["user_id"] = request.user_id
    update_document = {
        '$set': {
            'user': request.user_name,
        }
    }
    try:
        collection = await dbconnect("practice_user","practice_user")
        print("connected to update the record")
        update_result = collection.update_one(filter, update_document)
    except Exception as e:
        print("connection lost",e)
    output = await get_user_data()
    return output




