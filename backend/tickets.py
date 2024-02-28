from fastapi import APIRouter,Request,HTTPException
from models import *
from mongo import *
from jwt_auth import decodeJWT

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
    return {"msg" : "Ticket Raised Successfully"}