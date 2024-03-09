from fastapi import APIRouter
from use_case import chatbot
import model

router = APIRouter(
    prefix="/chatbot",
    tags=['CHATBOT']
)


@router.post('/send_message')
def chatbot_controller(data: model.Message):
    return chatbot.chatbot_interface(data.message)
    
