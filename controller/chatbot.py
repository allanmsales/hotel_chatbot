from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from use_case import chatbot
import model


templates = Jinja2Templates(directory="templates")

router = APIRouter(
    prefix="/chatbot",
    tags=['CHATBOT']
)


@router.post('/send_message')
def chatbot_controller(data: model.Message):
    return chatbot.chatbot_interface(data.message)


@router.get('/front', response_class=HTMLResponse)
async def chatbot_front_controller(request: Request):
    first_question = "Hello! It's a pleasure to talk to you. I'll help you with your booking process. Could you please tell me your name?"
    return templates.TemplateResponse("chatbot.html", {"request": request, "first_question": first_question})
    
