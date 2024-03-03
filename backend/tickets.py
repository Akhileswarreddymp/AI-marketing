from fastapi import APIRouter,Request,HTTPException
from models import *
from mongo import *
from jwt_auth import decodeJWT
from bson.objectid import ObjectId

router = APIRouter()


@router.post('/raise_ticket',tags=["Tickets"])
async def create_ticket(request : tickets,auth:Request):
    try:
        token = auth.headers.get('access_token').split("Bearer ")[1]
        print(token)
        payload = decodeJWT(token)
        user_id = payload.get("userId")
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid token")
    if not isinstance(request,dict):
        data = dict(request)
    else:
        data = request
    collection = await dbconnect('Tickets','ticket')
    ticket_data = {
        "mailid" : user_id,
        "ticket_title" : data.get("title"),
        "priority" : data.get("priority"),
        "ticket_description" : data.get("description"),
        "ph_number" : data.get("number")
    }
    create_ticket = collection.insert_one(ticket_data)
    return {"msg" : "Ticket Created"}

@router.get("/get_tickets",tags=["Tickets"])
async def get_tickets(auth:Request):
    try:
        token = auth.headers.get('access_token').split("Bearer ")[1]
        print(token)
        payload = decodeJWT(token)
        user_id = payload.get("userId")
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid token")
    query= {'mailid': user_id}
    collection = await dbconnect('Tickets','ticket')
    get_ticket = collection.find(query)
    user_data = []
    for doc in get_ticket:
        doc['_id'] = str(doc['_id'])
        user_data.append(doc)
    return user_data


@router.delete("/deleteTicket",tags=["Tickets"])
async def deleteTicket(request : deleteTicket):
    query1= {'_id': ObjectId(request.id)}
    collection = await dbconnect('Tickets','ticket')
    
    delete_user = collection.delete_one(query1)
    print(delete_user)
    return {"msg":"Note Deleted"}

@router.put("/updateTicket",tags=["Tickets"])
async def updateTicket(request : updateTicket):
    if not isinstance(request,dict):
        data = dict(request)
    else:
        data = request
    update_document = {
        '$set': {
            "ticket_title" : data.get("title"),
            "priority" : data.get("priority"),
            "ticket_description" : data.get("description"),
            "ph_number" : data.get("number")
        }
    }
    query1= {'_id': ObjectId(request.id)}
    collection = await dbconnect('Tickets','ticket')
    delete_user = collection.update_one(query1,update_document)
    return {"msg":"Ticket Updated"}