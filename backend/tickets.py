from fastapi import APIRouter
from models import *
from mongo import *
router = APIRouter()


@router.post('/raise_ticket',tags=["Tickets"])
async def create_ticket(request : tickets):
    if not isinstance(request,dict):
        data = dict(request)
    else:
        data = request
    collection = await dbconnect('Tickets','ticket')
    ticket_data = {
        "ticket_title" : data.get("title"),
        "priority" : data.get("priority"),
        "ticket_description" : data.get("description"),
        "ph_number" : data.get("number")
    }
    create_ticket = collection.insert_one(ticket_data)
    return {"msg" : "Ticket Raised Successfully"}